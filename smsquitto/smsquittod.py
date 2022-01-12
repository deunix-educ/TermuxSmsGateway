#
# encoding: utf-8
import atexit
import sys, os
import datetime
import json
import ssl
import subprocess
import paho.mqtt.client as mqtt
import yaml

def yaml_load(f):
    with open(f, 'r') as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)
    return {}


class ClientMQTTBase(mqtt.Client):
    def __init__(self,
            host='localhost',
            port=1883,
            keepalive=60,
            username=None,
            password=None,
            useSSL=False,
            ca_cert=None,
            apikey='0192837495867'
        ):

        super(ClientMQTTBase, self).__init__()
        self.host = host
        self.port = port
        self.keepalive = keepalive
        if username:
            self.username_pw_set(username, password)

        if useSSL and ca_cert:
            self.tls_set(ca_certs=ca_cert, tls_version=ssl.PROTOCOL_TLSv1_2)
            #self.tls_insecure_set(True)

        self.topic = '%s/emit/' % apikey
        self.subscriptions = [['%s/pub/#' % apikey, 0],]

    def now(self):
        return int(datetime.datetime.now().timestamp())

    def sub(self):
        subs = [(topic, qos) for topic, qos in self.subscriptions]
        return subs

    def unsub(self):
        return [topic for topic, _ in self.subscriptions ]

    def startMQTT(self):
        self.connect(self.host, self.port, self.keepalive)
        self.subscribe(self.sub())

    def stopMQTT(self):
        self.unsubscribe(self.unsub())
        self.disconnect()
        self.exit()

    def publish_message(self, topic, **payload):
        try:
            qos = payload.pop('qos', 0)
            retain = payload.pop('retain', False)
            message = json.dumps(payload)
            self.publish(topic, payload=message.encode('utf_8'), qos=qos, retain=retain)
        except Exception as e:
            print("ClientMQTTBase::publish_message error:", e, flush=True)

    def on_connect(self, mqttc, obj, flags, rc):  # @UnusedVariable
        #print("ClientMQTTBase on_connect ")
        pass

    def on_message(self, mqttc, obj, msg):
        #print("ClientMQTTBase on_message:", msg.topic, msg.qos, msg.payload)
        pass

    def on_publish(self, mqttc, obj, mid):
        #print("on_publish:", mid, obj)
        pass

    def on_subscribe(self, mqttc, obj, mid, granted_qos):  # @UnusedVariable
        #print("ClientMQTTBase on_subscribe:", mid, granted_qos)
        pass

    def on_unsubscribe(self, mqttc, userdata, mid):  # @UnusedVariable
        #print("ClientMQTTBase on_unsubscribe:", mid, userdata)
        pass

    def on_disconnect(self, mqttc, userdata, mid):  # @UnusedVariable
        #print("ClientMQTTBase on_disconnect:", mqttc)
        pass

    def on_log(self, mqttc, obj, level, string):  # @UnusedVariable
        #print("onlog:", level, string)
        pass


class SmsQuitto(ClientMQTTBase):

    def __init__(self, **mosquitto):
        super(SmsQuitto, self).__init__(**mosquitto)

    def exit(self):
        self.gw_publish('stop', msg='SmsQuitto service stop!')

    def fetchSMS(self, mtype='inbox'):
        p = subprocess.Popen(["termux-sms-list", "-t", mtype], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        msg = p.stdout.read()
        payload = json.loads(msg.decode("utf-8"))
        for p in payload:
            evt = p.pop('type')
            dte = p.pop('received')
            time = datetime.datetime.strptime(dte, '%Y-%m-%d %H:%M').timestamp()
            self.publish_message(self.topic + evt, time=time, **p)

    def fetchLocation(self):
        p = subprocess.Popen("termux-location", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        msg = p.stdout.read()
        payload = json.loads(msg.decode("utf-8"))
        self.publish_message(self.topic + 'location', time=self.now(), **payload)

    def notification(self, title, msg):
        subprocess.run(["termux-notification", "--sound", '--title', title, '--content', msg])
        #print("SmsQuitto::notification", title, msg, flush=True)

    def sendSMS(self, mobile, text):
        subprocess.run(["termux-sms-send", "-n", mobile, text])
        print("SmsQuitto::sendSMS", mobile, text, flush=True)

    def gw_publish(self, evt, **payload):
        self.publish_message(self.topic + evt, time=self.now(), **payload)
        #print("SmsQuitto::gw_publish topic: %s payload: %s"% (self.topic+evt, payload), flush=True)

    def on_connect(self, mqttc, obj, flags, rc):  # @UnusedVariable
        self.gw_publish('start', msg='SmsQuitto service started!')
        self.notification('SmsQuitto', 'Service started!')
        #print("SmsQuitto::on_connect SmsQuitto service started!", flush=True)

    def on_disconnect(self, mqttc, obj, flags, rc):  # @UnusedVariable
        self.gw_publish('off', msg='SmsQuitto disconnected!')
        self.notification('SmsQuitto', 'Service disconnected!')
        #print("SmsQuitto::on_connect SmsQuitto service disconnected!", flush=True)

    def on_message(self, mqttc, obj, msg):  # @UnusedVariable
        try:
            topic = msg.topic
            evt = topic.rsplit('/', 1)[1]
            payload = json.loads(msg.payload.decode("utf-8"))
            if evt == 'sms':
                mobile = payload.get('mobile', None)
                text = '%s\n%s' % (payload.get('subject', ''), payload.get('msg', ''))
                if mobile:
                    if not isinstance(mobile, list):
                        mobile = [mobile]
                    for mob in mobile:
                        self.sendSMS(mob, text)

            elif evt == 'location':
                self.fetchLocation()

            elif evt in ['all','inbox','sent','draft','outbox']:
                self.fetchSMS(evt)

            elif evt == 'notify':
                title = payload.get('subject', '')
                text = payload.get('msg', '')
                self.notification(title, text)

            elif evt == 'kill-service':
                self.stopMQTT()

        except Exception as e:
            self.gw_publish('error', msg=str(e))
            print("SmsQuitto::on_message error:", e)

def main(path):
    try:
        pf = path[0] if path else os.path.dirname(os.path.abspath(__file__))
        config = yaml_load(os.path.join(pf, 'smsquitto-conf.yaml'))
        settings = dict(config.get('settings'))

        daemon = SmsQuitto(**settings)
        atexit.register(daemon.stopMQTT)
        daemon.startMQTT()
        daemon.loop_forever()

    except Exception as e:
        print("smsquitto.main error", e)

if __name__ == '__main__':
    main(sys.argv[1:])

#
