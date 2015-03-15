#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import urllib.request

def _post(path, data):
    resp = urllib.request.Request(
        "https://authserver.mojang.com" + path,
        json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8"
        }
    )
    return json.loads(urllib.request.urlopen(resp).read().decode("utf-8"))

def _build_repo(response):
    profile = response["selectedProfile"]
    return {
        "access_token": response["accessToken"],
        "client_token": response["clientToken"],
        "uuid": profile["id"],
        "name": profile["name"],
        "legacy": profile["legacy"]
    }

def login(username, password):
    response = _post(
        "/authenticate",
        {
            "agent": {
                "name": "Minecraft",
                "version": 1
            },
            "username": username,
            "password": password
        }
    )
    return _build_repo(response)

def refresh(repo):
    response = _post(
        "/refresh",
        {
            "accessToken": repo["access_token"],
            "clientToken": repo["client_token"]
        }
    )
    return _build_repo(response)
