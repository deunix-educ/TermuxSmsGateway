# termux-sms-gateway
SMS and notification gateway from Android smartphone

#### Goal:

Make any laptop with an Internet connection an SMS gateway
Send SMS from his desktop from a web interface or other.
Receive SMS on his desk in order to use the content.

#### Method used

- SMS sending

- SMS are created on one machine (1 or more) on the network.
    - They are then published to a public or private MQTT server
    - The messages are received on an MQTT client installed on the laptop (1 or more).
    - The messages are then sent to the recipients.

#### SMS reception

- The SMS are received on the mobile and published to the MQTT server
- The messages are received on an MQTT client installed on the subscribed machine (1 or more)

#### Conditions for receiving or sending

- Take a public or private MQTT server to relay messages
- Subscribe MQTT clients to the same topics

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

#### Non-exhaustive use
- Complement of the email message
- Receive and process alert messages (IOT or other)
- etc ...

### Installation

https://github.com/termux/termux-app

#### Installation of termux
- Termux application obtained by F-Droid:
    - https://www.f-droid.org/fr/

- Or by google store:
    - https://play.google.com/

> IMPORTANT: We will choose either one or the other.

- Install
    - Termux
    - Termux: API
    - Termux: Widget

#### Installing the mqtt client:

The following python packages will be installed:

- termux-sms-gateway
- paho-mqtt
- rsa >> https://stuvel.eu/python-rsa-doc/

### Installation procedure

After installing termux on the laptop, launch Termux

- Copy and paste the following command in the terminal

        export PACKAGE="TermuxSmsGateway"&&export VERSION="1.0"&&mkdir -p $HOME/.termux/tasks&&
        apt install termux-api git -y&&rm -rf termux-sms-gateway&&
        git clone &&
        cp -f $PACKAGE/smsquitto-st* $HOME/.termux/tasks/&&cp -f $PACKAGE/smsquitto/smsquitto-conf.yaml $HOME/.termux/&&
        pip install $PACKAGE/dist/smsquitto-$VERSION.tar.gz

- Enter to start the installation

### Installation parameters

- The installation parameters are in ~ / .termux / smsquitto-conf.yaml
    - host: ip or domain of the MQTT server
    - port: 1883 or 8883
    - keepalive: 60
    - username: login
    - password: password
    - useSSL: False or True
    - ca_cert: path/of/file/ca.cert
    - apikey: *string*

        - ** IMPORTANT **: This key is used to synchronize the topics with the subscriptions
            - ex: SQTT010203040506079

- Copy and paste the following command in the terminal

        nano $HOME/.termux/smsquitto-conf.yaml

- Install the service

     - Install the Tremux widget:Widget on the phone's desktop by keeping your finger on the screen
     - Choose shortcut
     - Change the icon and the name if you want
     - Start the service by clicking the icon

### Uses

- An MQTT client is required to operate the phone.
    - The smsquittod.py module gives an example of a client written in python.
        - The library used is that of the Eclipse foundation: pahon-mqtt
        - It will suffice to implement the ClientMQTTBase class

    - The sms-client-test.html file is another example but in websocket mode.
        - It will suffice to directly modify the html file
        - we launch it directly in a browser
            - by drag and drop
            - by an address of this type
                - file: ///path/du/fichier/sms-client.html

- demonstration

     - sms-client-test.html is fully functional
     - You just have to update the apikey in this file and in the configuration file on the mobile phone
     - And set up some mobile numbers to do the tests

### Domotiz

- https://www.domoticz.com/wiki/Getting_started

- Send notification from custom HTTP/Action

    - Notification
        - script://notify.sh #FIELD1 #FIELD2 #FIELD3 #FIELD4 #TO #MESSAGE --tls or nothing
            - /usr/bin/python3 /home/pi/domoticz/scripts/notify.py --method=notify --host=$1 --port=$2 --user=$3 --password=$4 --apikey=$5 --text="$6" $7

    - SMS
        - script://notify.sh #FIELD1 #FIELD2 #FIELD3 #FIELD4 #TO #MESSAGE "00330645953706,0033791246318" --tls or nothing
            - /usr/bin/python3 /home/pi/domoticz/scripts/notify.py --method=sms --host=$1 --port=$2 --user=$3 --password=$4 --apikey=$5 --text="$6" --phone="$7" $8

    - SSL certification
        - argument --tls, in $7 or $8.
        - the certification key is in domoticz/scripts/notify.py. Thinking of modifying it.

    - You must install python3 paho-mqtt library: pip3 install paho-mqtt

### Orders

Messages sent and received on the phone are in this form

- (topic, payload)
    - topic: is a character string that starts with apikey see above
        - apikey/pub/sms
        - apikey/emit/inbox
    - payload: is a Json string
        - {mobile: [mobile1, mobile2, etc ...], subject: "the subject", msg: "the message"}
        - {time: time, payload: payload}
- orders
    - apikey/pub/sms send an sms
    - apikey/pub/notify send notification to phone
    - apikey/pub/location request for Geographic positioning
    - apikey/pub/inbox or all or sent or draft or outbox Read SMS
    - apikey/pub/kill-service stop the service on the phone
