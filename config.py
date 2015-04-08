#!/usr/bin/env python3

import json
import os.path

config_file = os.path.expanduser("~/.config/mcl.json")
if os.path.isfile(config_file):
    with open(config_file) as f:
        config = json.load(f)
else:
    config = {}

def save():
    with open(config_file, "w") as f:
        json.dump(config, f)
