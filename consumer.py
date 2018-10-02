#!/usr/bin/python3

import argparse
import json

from configuration import Configuration
from get_accounting import get_usage_records, store_usage_records

if __name__ == '__main__':
    config = Configuration()

    endpoints = json.load(open(config.get('services')))
    for e in endpoints:
        if not "endpoint" in endpoints[e]:
            continue

        try:
            usage_records = get_usage_records(e)
            store_usage_records(usage_records)
        except:
            # Ehm ...
            pass
