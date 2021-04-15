//===================================================================
/*
 * My Web mqtt client
 *
 * Copyright (c) 2018 deunix@e-educ.fr
 *
 *  MIT License
 *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy
 *  of this software and associated documentation files (the "Software"), to deal
 *  in the Software without restriction, including without limitation the rights
 *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 *  copies of the Software, and to permit persons to whom the Software is
 *  furnished to do so, subject to the following conditions:
 *
 *  The above copyright notice and this permission notice shall be included in all
 *  copies or substantial portions of the Software.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 *  SOFTWARE.
 */
//======================================================
// some useful functions
function toFloat(value, n) {
    return parseFloat(value).toFixed(n);
}

function toDecimal(value, n) {
    return parseInt(value).toFixed(n);
}

function b64_to_utf8( str ) {
  return decodeURIComponent(escape(window.atob( str )));
}

function format_date(unixtimestamp) {
    var date = new Date(1000*parseInt(unixtimestamp));
    var dateString =
    date.getUTCFullYear() + "/" +
    ("0" +(date.getUTCMonth()+1)).slice(-2)+ "/" +
    ("0" + date.getUTCDate()).slice(-2) + " " +
    ("0" + date.getUTCHours()).slice(-2) + ":" +
    ("0" + date.getUTCMinutes()).slice(-2) + ":" +
    ("0" + date.getUTCSeconds()).slice(-2);
  return dateString;
}
function locale_date(unixtimestamp) {
  var date = new Date(1000*parseInt(unixtimestamp));
  var dateString =
  date.getFullYear() + "/" +
  ("0" +(date.getMonth()+1)).slice(-2)+ "/" +
  ("0" + date.getDate()).slice(-2) + " " +
  ("0" + date.getHours()).slice(-2) + ":" +
  ("0" + date.getMinutes()).slice(-2) + ":" +
  ("0" + date.getSeconds()).slice(-2);
  return dateString;
}

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;
    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
}

var MQTT_RETAIN     = true;
var MQTT_NO_RETAIN  = false;
var QOS_AT_MOST_ONCE  = 0;
var QOS_AT_LEAST_ONCE = 1;
var QOS_EXACTLY_ONCE  = 2;

var MqttClientClass = function MqttClient(options, callbacks) {
    var self = this;
    var defaults = {
        host: "127.0.0.1",
        port: 1884,
        reconnectTimeout: 5,    // seconds
        subs: [],
        datas: [],
        //
        userName: null,
        password: null,
        onSuccess: onConnect,
        onFailure: onFailure,
        useSSL: false,
        cleanSession: true,
        timeout: 30,
        keepAliveInterval: 60,
    };

    var defaultCallbacks = {
        onMessageCallback: onMessageArrived,
        onConnectionLostCallback: onConnectionLost,
        onConnectionCallback: null,
        onDisconnectionCallback: null,
        onSubscribeCallback: null,
        onPublishCallback: null,
        onSynMessageCallback: null,
        onAckMessageCallback: null,
        onPongMessageCallback: null,
    };
    var mqtt = null;
    var opt = $.extend(defaults, options);
    var cbk = $.extend(defaultCallbacks, callbacks);
    var reconnectTimeout = opt.reconnectTimeout * 1000; delete opt.reconnectTimeout;

    this.callbacks = cbk;
    this.datas = opt.datas; delete opt.datas;
    this.clid = "pahoJsCli_" + $.now();
    this.host = opt.host; delete opt.host;
    this.port = opt.port; delete opt.port;
    this.subs = opt.subs; delete opt.subs;

    // private methods
    //
    function MQTTconnect() {
        mqtt = new Paho.MQTT.Client(self.host, self.port, self.clid);
        mqtt.onConnectionLost = cbk.onConnectionLostCallback;
        mqtt.onMessageArrived = cbk.onMessageCallback;
        mqtt.connect(opt);
    }

    function MQTTsubscribe() {
        $.each(self.subs, function(i, sub) {
            mqtt.subscribe(sub[0], {qos: sub[1]});
            if (cbk.onSubscribeCallback)
                (cbk.onSubscribeCallback(sub[0], sub[1]));
        });
    }

    function onFailure(message) {
        //console.log("Connection failed: " + message.errorMessage + ". Retrying...");
        setTimeout(MQTTconnect, reconnectTimeout);
    }

    function onConnect() {
        //console.log('Connected to ' + self.host + ':' + self.port + "\nId: "+ self.clid);
        if (cbk.onConnectionCallback)
            cbk.onConnectionCallback();
        MQTTsubscribe();
    }

    function onConnectionLost(response) {
        if (cbk.onDisconnectionCallback)
            cbk.onDisconnectionCallback(response);
        console.log("Connection lost: " + response.errorMessage + ". Reconnecting...");
        setTimeout(MQTTconnect, reconnectTimeout);
    }

    function onMessageArrived(message) {
        var topic = message.destinationName;
        var payload = message.payloadString;
        console.log(topic +"\n"+ payload);
    }

    function MQTTpublish(topic, payload, qos, retained) {
        if (cbk.onPublishCallback)
            cbk.onPublishCallback(payload);
        mqtt.send(topic, payload, qos, retained);
    }

    function MQTTdeleteRetainedMessage(topic) {
        mqtt.send(topic, "", 0, true);
    }

    function MQTTpublishMessage(topic, payload) {
        var msg = (typeof payload == 'undefined' || payload == null) ? {evt: topic}: payload;
        MQTTpublish(topic, JSON.stringify(msg), QOS_AT_LEAST_ONCE, MQTT_NO_RETAIN);
    }

    // public methods
    //
    this.connect     = function()                               { MQTTconnect();            };
    this.disconnect  = function()                               { mqtt.disconnect();        };
    this.isConnected = function()                               { return mqtt.connected;    };
    this.suscribe    = function(filter, subscribeOptions)       { mqtt.suscribe(filter, subscribeOptions);      };
    this.unsubscribe = function(filter, unsubscribeOptions)     { mqtt.unsuscribe(filter, unsubscribeOptions);  };
    this.publish     = function(topic, payload, qos, retained)  { MQTTpublish(topic, payload, qos, retained);   };
    this.publishMessage = function(topic, payload)              { MQTTpublishMessage(topic, payload);           };
    this.deleteRetainedMessage = function(topic)                { MQTTdeleteRetainedMessage(topic);             };
};
