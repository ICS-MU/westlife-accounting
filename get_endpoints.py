#!/usr/bin/python3

import requests
import json
import argparse
import logging
import csv
import sys

from configuration import Configuration

def do_http(url):
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

    return(response.text)

def get_endpoints():
    endpoints=dict()
    with open(config.get("services_endpoints"), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            endpoints[row["saml_entity_id"]] = row["accounting_endpoint"]

    services = do_http(config.get("services_url"))

    js = json.loads(services)
    for service in js:
        if not service in endpoints:
            print("Service '%s' doesn't have a known endpoint (check %s)" % (service, config.get("services_endpoints")),
                file=sys.stderr)
            continue
        js[service]["endpoint"] = endpoints[service]

    print(json.dumps(js))


def parse_args():
    parser = argparse.ArgumentParser(
            description="Obtain the endpoints to gather accounting data from")

    return parser.parse_args()

config = Configuration()

if __name__ == '__main__':
    args = parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    get_endpoints()
