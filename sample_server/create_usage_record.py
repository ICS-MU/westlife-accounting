#!/usr/bin/python3

import os
import sys
import jwt
import json
import argparse

def get_user_record():
    return(json.load(sys.stdin))

def generate_record(privkey):
    with open(privkey) as f:
        key = f.read()
        encoded = jwt.encode(get_user_record(), key, algorithm='RS256')
    os.write(sys.stdout.fileno(), encoded)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate signed usage record")
    parser.add_argument('privkey', help="The signature key (should be from SAML metadata)")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    generate_record(args.privkey)
