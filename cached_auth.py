#!/usr/bin/env python3

import config
import auth

def authenticate(username):
    if "profiles" not in config.config:
        config.config["profiles"] = {}
    if username in config.config["profiles"]:
        profile = config.config["profiles"][username]
        profile = auth.refresh(profile)
        config.config["profiles"][username] = profile
        config.save()
        return profile
    import getpw
    pw = getpw.getpw("Password", "Password for '%s': " % username)
    profile = auth.login(username, pw)
    config.config["profiles"][username] = profile
    config.save()
    return profile
