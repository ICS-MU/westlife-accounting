#!/usr/bin/python3

import jwt
import os
import requests
import json
import logging
import base64
import tempfile
import argparse
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

from configuration import Configuration
from db import Database
from ur import UsageRecord, parse_usage_record

def lookup_public_key(name=None):
    kouril = '''\
-----BEGIN CERTIFICATE-----
MIIFrDCCBJSgAwIBAgIQBLJvHj45id6hybVQjV01qjANBgkqhkiG9w0BAQsFADBy
MQswCQYDVQQGEwJOTDEWMBQGA1UECBMNTm9vcmQtSG9sbGFuZDESMBAGA1UEBxMJ
QW1zdGVyZGFtMQ8wDQYDVQQKEwZURVJFTkExJjAkBgNVBAMTHVRFUkVOQSBlU2Np
ZW5jZSBQZXJzb25hbCBDQSAzMB4XDTE3MTExNTAwMDAwMFoXDTE4MTIxNDEyMDAw
MFowgYkxEzARBgoJkiaJk/IsZAEZFgNvcmcxFjAUBgoJkiaJk/IsZAEZFgZ0ZXJl
bmExEzARBgoJkiaJk/IsZAEZFgN0Y3MxCzAJBgNVBAYTAkNaMRswGQYDVQQKExJN
YXNhcnlrIFVuaXZlcnNpdHkxGzAZBgNVBAMTEkRhbmllbCBLb3VyaWwgMTM4ODCC
ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALcKXkFNRj9xL5c6ExhphTiw
wO6Lc6xWaY8alqKxrLa/ZNJtWrQkeWnnF2LrUwqWGSbLg3GGcmvTbEgF9GNTnO2s
T+e1rCLsGUmOgmNUKWE/VKm7iEup7fcIiZButbcETmHL39OrE4IULIoeSk3NUSTc
NFEpYQgYHYfmfPtJUhyKFGCwcsZZEUEa+Q2fKyBJWiTcugJSFAMF1j8WIo9cBFOH
rVbVtQJazwP7HrDhFwU5LnR/oSG+1BpWuuz0LPbRLQqXKEzRj6zbcxgZPn6GcJSL
kMBjdJUusVNrPLFPM5UQj0IGs6DNX5t/+GiRWZ+h3zxKuilKFtB3kM4eK6GyhWsC
AwEAAaOCAiQwggIgMB8GA1UdIwQYMBaAFIyfES7m43oEpR5Vi0YIBKbtl3CmMB0G
A1UdDgQWBBThrKU+8tahO0Bz1jBTMmIYWg9A4jAMBgNVHRMBAf8EAjAAMGYGA1Ud
EQRfMF2BDDEzODhAbXVuaS5jeoERMTM4OEBtYWlsLm11bmkuY3qBE2tvdXJpbEBt
YWlsLm11bmkuY3qBEmtvdXJpbEBpY3MubXVuaS5jeoERa291cmlsQGZpLm11bmku
Y3owDgYDVR0PAQH/BAQDAgSwMB0GA1UdJQQWMBQGCCsGAQUFBwMCBggrBgEFBQcD
BDA0BgNVHSAELTArMAwGCiqGSIb3TAUCAgEwDAYKYIZIAYb9bAQfATANBgsqhkiG
90wFAgMDAzCBhQYDVR0fBH4wfDA8oDqgOIY2aHR0cDovL2NybDMuZGlnaWNlcnQu
Y29tL1RFUkVOQWVTY2llbmNlUGVyc29uYWxDQTMuY3JsMDygOqA4hjZodHRwOi8v
Y3JsNC5kaWdpY2VydC5jb20vVEVSRU5BZVNjaWVuY2VQZXJzb25hbENBMy5jcmww
ewYIKwYBBQUHAQEEbzBtMCQGCCsGAQUFBzABhhhodHRwOi8vb2NzcC5kaWdpY2Vy
dC5jb20wRQYIKwYBBQUHMAKGOWh0dHA6Ly9jYWNlcnRzLmRpZ2ljZXJ0LmNvbS9U
RVJFTkFlU2NpZW5jZVBlcnNvbmFsQ0EzLmNydDANBgkqhkiG9w0BAQsFAAOCAQEA
INj1Gq1+cW/t3Oh/6sQlOUsKXOizpfB4Nxx//j+eaKoRCrbsMZnaTm1yzdH1Rr1K
nFE2Paa6j08/nmJ67ctwCgU1qJ7JPIvUJ3Ohj7N/HbOrJpjtzrYQuH7mw80fkUgf
yFYDIWupPQNuLFXFT38ThGAwGcDeyGuKs8RbNqfpcj04hClSGY2xBjGf4VE1lGO+
eEoNbGh6CF/h9I2YIkyj6/6P7zgDaN+fQDMnLP6Ku+ZkU+xqyrWeV5ElmlYz61Mk
LLAm2JZXaPMVaLp27z94CBkot4+8b1xRIaXfvCm0Z6buzk7zvAy10cQmlyh8g2X4
HZ8IRSmV16XBspkcZmyP+Q==
-----END CERTIFICATE-----
'''
    cert_obj = load_pem_x509_certificate(kouril.encode('ascii'), default_backend())
    return(cert_obj.public_key())


def extract_usage_records(token):
    signer = lookup_public_key()
    msg = jwt.decode(token, signer, algorithms='RS256')

    if msg["status"] != "success":
        error = msg["error"] if "error" in msg else "Unknown error"
        logging.error("Server failed to return the record (%s)", error)
        raise Exception("Server failed to return the record (%s)", error)

    usage_records = list()
    for ur in msg["data"]:
        usage_records.append(parse_usage_record(ur))

    return usage_records


def get_usage_records(url):
    cert = config.get("cert")
    key = config.get("key")
    if cert is None or key is None:
        logging.error("The configuration doesn't specify authentication certificate or private key")
        raise Exception("Both cert and key must be specified")

    verify = config.get("cadir") if config.get("cadir") is not None else True
        
    requests_logger = logging.getLogger("urllib3")
    requests_logger.setLevel(logging.ERROR)
    response = requests.get(url, verify=verify, cert=(cert, key))

    if response.status_code != 200:
        logging.error("Failed to get response from %s: (%d: %s)" %
            (url, response.status_code, response.reason))
        raise Exception("Failed to get HTTP response")

    return (extract_usage_records(response.text.rstrip(os.linesep)))

def parse_args():
    parser = argparse.ArgumentParser(
            description="Obtain a set of usage records from a service")
    parser.add_argument('url', help="Endpoint to get usage records from")

    return parser.parse_args()


config = Configuration()

if __name__ == '__main__':
    args = parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    usage_records = get_usage_records(args.url)
    db = Database()
    for ur in usage_records:
        db.store_ur(ur)
