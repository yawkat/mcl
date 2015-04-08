#!/usr/bin/env python3

import config
import cached_auth

from util import *

def launch(profile, binary, server):
    cmdline = [
        binary,
        "--username", profile["name"],
        "--uuid", profile["uuid"],
        "--accessToken", profile["access_token"],
        "--server", server,
    ]

    log("Command line: " + " ".join(cmdline), 90)

    import subprocess
    subprocess.call(cmdline)

def main():
    import argparse

    parser = argparse.ArgumentParser()
    default_binary = None
    if "steven_binary" in config.config:
        default_binary = config.config["steven_binary"]
    parser.add_argument("username", nargs=1)
    parser.add_argument("server", nargs=1)
    parser.add_argument("--binary", default=default_binary, required=(default_binary is None))
    args = parser.parse_args()
    if args.binary != default_binary:
        config.config["steven_binary"] = args.binary
        config.save()

    log("Binary:   %s" % args.binary)
    log("Server:   %s" % args.server[0])

    profile = cached_auth.authenticate(args.username[0])

    log("Username: %s" % profile["name"])
    log("UUID:     %s" % profile["uuid"])

    launch(profile, args.binary, args.server[0])

if __name__ == '__main__':
    main()
