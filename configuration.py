#!/usr/bin/python3

import sys

class Configuration:
    def __init__(self, path="/etc/westlife-accounting"):
        # there's no way to prepend a directory
        sys.path = [path] + sys.path
        import config as c
        self.config = c.CONFIG

    def get(self, key):
        if not key in self.config:
            return None
        return self.config[key]
