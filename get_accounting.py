#!/usr/bin/python3

import jwt
import os
import sys
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

def lookup_service_url(name):
    endpoints = json.load(open(config.get('services')))
    return endpoints[name]["endpoint"]

def lookup_service_pubkey(name):
    endpoints = json.load(open(config.get('services')))
    cert = endpoints[name]["cert"]
    cert_obj = load_pem_x509_certificate(cert.encode('ascii'), default_backend())
    return(cert_obj.public_key())


def extract_usage_records(token, service):
    signer = lookup_service_pubkey(service)
    msg = jwt.decode(token, signer, algorithms='RS256')

    if msg["status"] != "success":
        error = msg["error"] if "error" in msg else "Unknown error"
        logging.error("Server failed to return the record (%s)", error)
        raise Exception("Server failed to return the record (%s)", error)

    usage_records = list()
    for ur in msg["data"]:
        usage_records.append(parse_usage_record(ur))

    return usage_records


def get_usage_records(service):
    cert = config.get("cert")
    key = config.get("key")
    if cert is None or key is None:
        logging.error("The configuration doesn't specify authentication certificate or private key")
        raise Exception("Both cert and key must be specified")

    verify = config.get("cadir") if config.get("cadir") is not None else True

    url = lookup_service_url(service)
        
    requests_logger = logging.getLogger("urllib3")
    requests_logger.setLevel(logging.ERROR)
    response = requests.get(url, verify=verify, cert=(cert, key))

    if response.status_code != 200:
        logging.error("Failed to get response from %s: (%d: %s)" %
            (url, response.status_code, response.reason))
        raise Exception("Failed to get HTTP response")

    token = response.text.rstrip(os.linesep)
    return (extract_usage_records(token, service))

def parse_args():
    parser = argparse.ArgumentParser(
            description="Obtain a set of usage records from a service")
    parser.add_argument('service', help="The service to get usage records from")

    return parser.parse_args()


config = Configuration()

if __name__ == '__main__':
    args = parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    usage_records = get_usage_records(args.service)
    db = Database()
    for ur in usage_records:
        db.store_ur(ur)
