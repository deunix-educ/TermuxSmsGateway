# termux-sms-gateway
SMS and notification gateway from Android smartphone

#### Goal:

Make any laptop with an Internet connection an SMS gateway
Send SMS from his desktop from a web interface or other.
Receive SMS on his desk in order to use the content.

#### Method used

- SMS sending

- SMS are created on one machine (1 or more) on the network.
    - They are then published to a public or private MQTT mail server
    - The messages are received on an MQTT client installed on the laptop (1 or more).
    - The messages are then sent to the recipients.

####SMS reception

- The SMS are received on the mobile and published to the MQTT server
- The messages are received on an MQTT client installed on the subscribed machine (1 or more)

#### Conditions for receiving or sending

- Take a public or private MQTT server to relay messages
- Subscribe MQTT clients to the same topics

#### Non-exhaustive use

- Email message usage
- Receive and process alert messages (IOT or other)
- etc ...
