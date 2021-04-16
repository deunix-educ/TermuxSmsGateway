# Termux Sms Gateway
Passerelle SMS et notification à l'aide d'un smartphone Android

#### But:

Faites de n'importe quel ordinateur portable avec une connexion Internet une passerelle SMS
Envoyez des SMS depuis son bureau en utilisant une interface web ou autre.
Recevoir des SMS sur son bureau afin d'utiliser le contenu.


#### Method used

#### Emission de SMS ou de Notification

- Les SMS sont créés sur une machine (1 ou plus) sur le réseau.
     - Ils sont ensuite publiés sur un serveur MQTT public ou privé
     - Les messages sont reçus sur un client MQTT installé sur l'ordinateur portable (1 ou plus).
     - Les messages sont ensuite envoyés aux destinataires.


#### Réception de SMS

- Les SMS sont reçus sur le smartphone et publiés sur le serveur MQTT
- Les messages sont reçus sur un client MQTT installé sur la machine abonnée (1 ou plus)

#### Utilisation non exhaustive

- Utilisation des e-mails
- Recevoir et traiter les messages d'alerte (IOT ou autre)
- etc ...

#### Conditions de réception ou d'envoi

- Prenez un serveur MQTT public ou privé pour relayer les messages
- Abonnez les clients MQTT aux mêmes sujets

> Vous pouvez installer votre propre serveur mosquitto
>> https://mosquitto.org/download/
>
> Plus d'informations sur MQTT: https://fr.wikipedia.org/wiki/MQTT

- Sécurité des données transmises
> Nous pouvons avoir besoin de crypter le contenu pour des raisons de sécurité.
>> Utiliser le cryptage avec clé publique / clé privée sur les clients

### Installation sur le Smartphone

https://github.com/termux/termux-app

#### Installation de Termux
- Termux sur F-Droid:
    - https://www.f-droid.org/fr/

- Ou sur google store:
    - https://play.google.com/

> IMPORTANT: Vous devez choisir l'un ou l'autre dépôt

- Installer
    - Termux
    - Termux: API
    - Termux: Widget

#### Installation du client MQTT

Les packages python suivants seront installés:

- smsquitto la passerelle sms
- paho-mqtt
- supervisor
- le superviseur est un système de contrôle de processus
	- parce qu'Android ne prend pas en charge les liens physiques, il sera nécessaire de patcher http.py à partir de la bibliothèque
- rsa >> https://stuvel.eu/python-rsa-doc/

### Procédure d'installation

Après avoir installé termux sur le smartphone, lancez Termux

- Copiez et collez la commande suivante dans le terminal Termux

        export PACKAGE="TermuxSmsGateway"&&
		export VERSION="1.0"&&
		mkdir -p $HOME/.termux/tasks&&
        apt install python git termux-api -y&&
		rm -rf TermuxSmsGateway&&
        git clone https://github.com/deunix-educ/TermuxSmsGateway.git&&
        cp -f $PACKAGE/smsquitto-install/smsquitto-st* $HOME/.termux/tasks/&&
		cp -f $PACKAGE/smsquitto/smsquitto-conf.yaml $HOME/.termux/&&
		cp -f $PACKAGE/smsquitto-install/supervisor/supervisord $HOME/.termux/boot/&&
		cp -f $PACKAGE/smsquitto-install/supervisor/supervisord.conf $PREFIX/etc/&&
		cp -f $PACKAGE/smsquitto-install/supervisor/smsquitto.conf $PREFIX/etc/supervisor.d/&&
        pip install $PACKAGE/dist/smsquitto-$VERSION.tar.gz&&
		cd $PREFIX/lib/python3.9/site-packages/supervisor&&
		patch < $PACKAGE/smsquitto-install/supervisor/patch/http.py.patch

- Entrez pour démarrer l'installation

### Configuration du server

- configuration smsquitto >> ~/.termux/smsquitto-conf.yaml
    - host: ip or domain serveur MQTT
    - port: 1883 or 8883
    - keepalive: 60
    - username: login
    - password: password
    - useSSL: False or True
    - ca_cert: path/to/file/ca.cert
    - apikey: *string*

        - ** IMPORTANT **: Cette clé permet de synchroniser les rubriques avec les abonnements
            - ex: SQTT010203040506079

- Copiez et collez la commande suivante dans le terminal
        nano $HOME/.termux/smsquitto-conf.yaml

- Installation des services (start, stop, status)
- Installer le widget Tremux: Widget sur le téléphone en gardant votre doigt sur l'écran
      - Choisissez un raccourci
      - Changez l'icône et le nom si vous le souhaitez
      - Démarrez, arrêtez ou service d'état en cliquant sur l'icône

### Usage

- Un client MQTT est nécessaire pour faire fonctionner le téléphone.
     - Le module smsquittod.py donne un exemple de client écrit en python.
         - La bibliothèque est la fondation Eclipse paho-mqtt
         - Implémentez simplement la classe ClientMQTTBase

     - Le fichier sms-client.html est un autre exemple mais en mode websocket.
         - Modifiez directement le fichier sms-client.html
         - Lancez-le directement dans un navigateur
             - par glisser-déposer
             - par une adresse de ce type
                 - fichier: ///path/to/file/sms-client.html

- démonstration

      - sms-client.html est entièrement fonctionnel
      - Il vous suffit de mettre à jour l'apikey dans ce fichier et dans le fichier de configuration sur le smartphone
      - Configurer des numéros de mobile pour faire les tests

### Notification dans Domotiz

- https://www.domoticz.com/wiki/Getting_started

##### Ci-dessous le processus d'intégration

- Envoyer une notification depuis HTTP / Action personnalisé

     - Notification
		- script: //notify.sh # FIELD1 # FIELD2 # FIELD3 # FIELD4 #TO #MESSAGE --tls ou rien
		- commande
			- /usr/bin/python3 /home/pi/domoticz/scripts/notify.py --method=notify --host=$1 --port=$2 --user=$3 --password=$4 --apikey=$5 --text="$6" $7

    - SMS
        - script://notify.sh #FIELD1 #FIELD2 #FIELD3 #FIELD4 #TO #MESSAGE "00330645953706,0033791246318" --tls or nothing
			- command
            	- /usr/bin/python3 /home/pi/domoticz/scripts/smsquitto.py --method=sms --host=$1 --port=$2 --user=$3 --password=$4 --apikey=$5 --text="$6" --phone="$7" $8

    - SSL certification
        - argument --tls, in $7 or $8.
        - La clef de certification dans domoticz/scripts/smsquitto.py.

    - Vous devez installer la bibliothèque python3 paho-mqtt: pip3 install paho-mqtt

### Méthodes API
Format du message envoyé et reçu:

- (topic, payload)
    - topic:
        - apikey/pub/sms
        - apikey/emit/inbox
    - payload: chaîne qui commence par apikey voir ci-dessus
        - {mobile: [mobile1, mobile2, etc ...], subject: "the subject", msg: "the message"}
        - {time: time, payload: payload}
- topics
    - apikey/pub/sms --> envoi de  SMS
    - apikey/pub/notify --> émission de notification
    - apikey/pub/location --> positionnement Geographique
    - apikey/pub/inbox --> ou all or sent or draft or outbox Read SMS message
    - apikey/pub/kill-service --> stopper le service

