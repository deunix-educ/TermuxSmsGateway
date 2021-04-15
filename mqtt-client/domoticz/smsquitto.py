#!/usr/bin/python3
# encoding: utf-8
'''
notify -- termux notification
Send sms or notification to a smartphone
@author:     deunix
@contact:    deuxnix@e-educ.fr
'''

import os, sys, ssl, json

from argparse import ArgumentParser
import paho.mqtt.publish as publish

CA_CERTS = """
-----BEGIN CERTIFICATE-----
EAYDVQQKDAllLWVkdWMuZnIxDDAKBgNVBAsMA29yZzESMBAGA1UEAwwJZS1lZHVj
LmZyMR0wGwYJKoZIhvcNAQkBFg5yb290QGUtZWR1Yy5mcjAeFw0yMDA2MTUwNzMw
MjVaFw0zMDA2MTMwNzMwMjVaMH4xCzAJBgNVBAYTAkZSMQswCQYDVQQIDAJPQzEN
MAsGA1UEBwwEQUxCSTESMBAGA1UECgwJZS1lZHVjLmZyMQwwCgYDVQQLDANvcmcx
EjAQBgNVBAMMCWUtZWR1Yy5mcjEdMBsGCSqGSIb3DQEJARYOcm9vdEBlLWVkdWMu
ZnIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCesN2Xt6uKezWj55gK
qBxzqyIe06GQqerGXWMQhdP5KiSP1PKRZVBcZzze0A//Qcd/f204CTu1P5Qj9pcG
2LIgGiH5r89j2cyvKDtgbwYT2HdWAJtqnI1d9LWl2RLLaaKijmwJl0rhFdOojxsz
s09sdXq3aSkpYG8f5y166jRPOCusOC+OdnqOJObVUWYI25gQUJ4KYd13oMVmCB90
tsqpjLcWa3y/sZ7ngYJr2EzFDpGv299dqgw+fVuxeOgMvlCllw6mgXenegjyHRZP
9BS5742LIdDsc11BcA4bEW97+M7gZg/s0hPJim5oZqXdYJFZ5VFK7GQuyah3euHw
V97PAgMBAAGjUzBRMB0GA1UdDgQWBBRb1QVCTMLstcT9rClf106cLrK2lTAfBgNV
HSMEGDAWgBRb1QVCTMLstcT9rClf106cLrK2lTAPBgNVHRMBAf8EBTADAQH/MA0G
CSqGSIb3DQEBCwUAA4IBAQALmdJCtU3k5OKYkA3iiriW5NVya7XplmcGMg4KMtRL
E3kb6yS6sk7Msri1YNA/6noWSHAZIDfBmoadrCNm4XB/
-----END CERTIFICATE-----
"""

def publish_message(topic, payload, host='127.0.0.1', port=1883, auth={}, ca_certs=None):
    publish.single(topic, payload.encode('utf_8'), qos=0, hostname=host, port=port, auth=auth, \
            tls={'ca_certs': ca_certs, 'tls_version': ssl.PROTOCOL_TLSv1_2} if ca_certs else None,)

def main():
    try:
        parser = ArgumentParser()
        parser.add_argument("-H", "--host", dest="host", action="store", type=str, default="broker.emqx.io")
        parser.add_argument("-P", "--port", dest="port", action="store", type=int, default=1883)
        parser.add_argument("-u", "--user", dest="user", action="store", type=str, default='emqx')
        parser.add_argument("-p", "--password", dest="password", action="store", type=str, default='public')
        parser.add_argument("-a", "--apikey", dest="apikey", action="store", type=str, required=True)
        parser.add_argument("-m", "--method", dest="method", action="store", type=str, default='notify')
        parser.add_argument("-s", "--phone", dest="phone", action="store", type=str, default='')
        parser.add_argument("-t", "--text", dest="message", action="store", type=str, required=True)
        parser.add_argument("--tls", dest="ca_certs", action="store_true", default=False, help="--tls if ca certification")

        args = parser.parse_args()

        topic = args.apikey + '/pub/' + args.method
        payload = { 'msg':  args.message };
        if args.method=='sms':
            payload['mobile'] = args.phone.split(',')

        publish_message(
            topic,
            json.dumps(payload),
            host=args.host,
            port=args.port,
            auth={'username': args.user, 'password': args.password },
            ca_certs=CA_CERTS if args.ca_certs else None,
        )
        return 0
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print("notify error", e)
        return 2

if __name__ == "__main__":
    sys.exit(main())


