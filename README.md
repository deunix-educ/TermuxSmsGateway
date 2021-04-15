# Termux Sms Gateway
SMS and notification gateway using Android smartphone

#### Goal:

Send and receive SMS or notification to a smartphone destination from any desktop using a web interface or other client.

#### Method used

##### SMS emission

    - SMS or notifications are created on one machine (1 or more) on the net.
    - Messages are then published to a public or private MQTT server
    - Smsquitto MQTT client installed on the smartphone gateway (1 or more)
        - receive and send these messages to recipients.

#### SMS reception

    - SMS received on the smartphone gateway are published to a MQTT server.
    - A MQTT client installed on a machine (1 or more) that have subscribed to a valid topic receive these messages

#### Non-exhaustive use

    - Email message usage
    - Receive and process alert messages (IOT or other)
    - etc ...

#### Conditions for receiving or sending
- Take a public or private MQTT server to relay messages
- Subscribe MQTT customers to the same topics

> You can install your own mosquitto server
>> https://mosquitto.org/download/
>
> More information on MQTT: https://fr.wikipedia.org/wiki/MQTT

- Security of data transmitted
> We may need to encrypt the content for security reasons.
>> Use encryption with public key / private key on clients

### Smartphone installation

https://github.com/termux/termux-app

#### Termux installation
- Termux application obtained by F-Droid:
    - https://www.f-droid.org/fr/

- Or by google store:
    - https://play.google.com/

> IMPORTANT: You must choose either one or the other repository.

- Install
    - Termux
    - Termux: API
    - Termux: Widget

#### MQTT client installing:

The following python packages will be installed:

- termux-sms-gateway
- paho-mqtt
- supervisor
- rsa >> https://stuvel.eu/python-rsa-doc/


### Installation procedure

After installing termux on the laptop, launch Termux

- Copy and paste the following command in the termux terminal

        export PACKAGE="TermuxSmsGateway"&&export VERSION="1.0"&&mkdir -p $HOME/.termux/tasks&&
        apt install termux-api git -y&&rm -rf termux-sms-gateway&&
        git clone &&
        cp -f $PACKAGE/smsquitto-st* $HOME/.termux/tasks/&&cp -f $PACKAGE/smsquitto/smsquitto-conf.yaml $HOME/.termux/&&
        pip install $PACKAGE/dist/smsquitto-$VERSION.tar.gz

- Enter to start installation

### Installation parameters

- Installation parameters are in ~/.termux/smsquitto-conf.yaml
    - host: ip or domain of the MQTT server
    - port: 1883 or 8883
    - keepalive: 60
    - username: login
    - password: password
    - useSSL: False or True
    - ca_cert: path/to/file/ca.cert
    - apikey: *string*

        - ** IMPORTANT **: This key is used to synchronize the topics with the subscriptions
            - ex: SQTT010203040506079

- Copy and paste the following command in the terminal

        nano $HOME/.termux/smsquitto-conf.yaml

- Install services (start, stop, status)

     - Install the Tremux widget:Widget on the phone's desktop by keeping your finger on the screen
     - Choose shortcut
     - Change the icon and the name if you want
     - Start, Stop, or Status service by clicking the icon

### Uses

- A MQTT client is required to the phone.
    - The smsquittod.py module gives an example of a client written in python.
        - Library is the Eclipse foundation paho-mqtt
        - Simply implemente ClientMQTTBase class

    - The sms-client.html file is another example but in websocket mode.
        - Directly modify the sms-client.html file
        - Launch it directly in a browser
            - by drag and drop
            - by an address of this type
                - file: ///path/to/file/sms-client.html

- Demonstration

     - sms-client.html is fully functional
     - You just have to update the apikey in this file and in the configuration file on the smartphone
     - Set up some mobile numbers to do the tests

### Domotiz

- https://www.domoticz.com/wiki/Getting_started

- Send notification from custom HTTP/Action

    - Notification
        - script://notify.sh #FIELD1 #FIELD2 #FIELD3 #FIELD4 #TO #MESSAGE --tls or nothing
            - /usr/bin/python3 /home/pi/domoticz/scripts/notify.py --method=notify --host=$1 --port=$2 --user=$3 --password=$4 --apikey=$5 --text="$6" $7

    - SMS
        - script://notify.sh #FIELD1 #FIELD2 #FIELD3 #FIELD4 #TO #MESSAGE "00330645953706,0033791246318" --tls or nothing
            - /usr/bin/python3 /home/pi/domoticz/scripts/smsquitto.py --method=sms --host=$1 --port=$2 --user=$3 --password=$4 --apikey=$5 --text="$6" --phone="$7" $8

    - SSL certification
        - argument --tls, in $7 or $8.
        - the certification key is in domoticz/scripts/smsquitto.py.

    - You must install python3 paho-mqtt library: pip3 install paho-mqtt

### API methods

Message sent and received format:

- (topic, payload)
    - topic: is a string that starts with apikey see above
        - apikey/pub/sms
        - apikey/emit/inbox
    - payload: is a Json string
        - {mobile: [mobile1, mobile2, etc ...], subject: "the subject", msg: "the message"}
        - {time: time, payload: payload}
- topics
    - apikey/pub/sms send SMS
    - apikey/pub/notify send notification
    - apikey/pub/location request for Geographic positioning
    - apikey/pub/inbox or all or sent or draft or outbox Read SMS message
    - apikey/pub/kill-service stop the service
