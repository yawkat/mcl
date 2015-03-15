#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path
import json
import auth

game_dir = os.path.expanduser("~/.minecraft")

config_file = os.path.expanduser("~/.config/mcl.json")
if os.path.isfile(config_file):
    with open(config_file) as f:
        config = json.load(f)
else:
    config = {}

def log(msg, color=36):
    print(u"\u001b[" + str(color) + "m\u001b[1m" + msg + u"\u001b[0m")

def _save_config():
    with open(config_file, "w") as f:
        json.dump(config, f)

def authenticate(username):
    if "profiles" not in config:
        config["profiles"] = {}
    if username in config["profiles"]:
        profile = config["profiles"][username]
        profile = auth.refresh(profile)
        config["profiles"][username] = profile
        _save_config()
        return profile
    import getpw
    pw = getpw.getpw("Password", "Password for '%s': " % username)
    profile = auth.login(username, pw)
    config["profiles"][username] = profile
    _save_config()
    return profile

def launch(profile, version):
    with open(game_dir + "/versions/" + version + "/" + version + ".json") as f:
        version_info = json.load(f)

    main_jar = game_dir + "/versions/" + version + "/" + version + ".jar"
    classpath = ""
    if "mods" in config and version in config["mods"]:
        for mod in config["mods"][version]:
            log("Loading mod %s" % mod)
            classpath += mod + ":"
    if classpath == "":
        log("No mods loaded.")
    else:
        patched = game_dir + "/versions/" + version + "/" + version + "-unsigned.jar"
        if not os.path.isfile(patched):
            log("Patching minecraft jar for mod support...")
            import zipfile
            with zipfile.ZipFile(main_jar, "r") as zin:
                with zipfile.ZipFile(patched, "w") as zout:
                    for item in zin.infolist():
                        buf = zin.read(item.filename)
                        if item.filename.find("META-INF") != 0:
                            zout.writestr(item, buf)
        main_jar = patched

    classpath += main_jar
    for lib in version_info["libraries"]:
        if "rules" in lib:
            accept = True
            for rule in lib["rules"]:
                # skip rules bound to another os
                if "os" in rule and rule["os"]["name"] != "linux":
                    continue
                # apply rule
                if rule["action"] == "allow":
                    accept = True
                else:
                    accept = False
            if not accept:
                # skip library
                continue

        if "natives" in lib:
            # TODO: extract
            continue

        classpath += ":"
        classpath += game_dir + "/libraries/"
        lib_group = lib["name"].split(":")[0]
        lib_artifact = lib["name"].split(":")[1]
        lib_version = lib["name"].split(":")[2]
        classpath += lib_group.replace(".", "/") + "/"
        classpath += lib_artifact + "/"
        classpath += lib_version + "/"
        classpath += lib_artifact + "-" + lib_version + ".jar"

    cmdline = [
        "java",
        "-XX:+UseG1GC",
        "-Xmx512m",
        "-Dsun.java2d.noddraw=true",
        "-Dsun.java2d.d3d=false",
        "-Dsun.java2d.opengl=false",
        "-Dsun.java2d.pmoffscreen=false",
        "-Djava.library.path=%s/versions/%s/%s-natives" % (game_dir, version, version),
        "-cp",
        classpath,
        version_info["mainClass"]
    ]

    options = {
        "version_name": version,
        "game_directory": game_dir,
        "assets_root": game_dir + "/assets",
        "assets_index_name": version_info["assets"],
        "user_properties": "{}",
        "auth_access_token": profile["access_token"],
        "auth_uuid": profile["uuid"],
        "auth_player_name": profile["name"]
    }
    if profile["legacy"]:
        options["user_type"] = "legacy"
    else:
        options["user_type"] = "### TODO"
    for arg in version_info["minecraftArguments"].split(" "):
        for k, v in options.items():
            arg = arg.replace("${%s}" % k, v)
        cmdline.append(arg)

    cmdline = [x.replace("$game_dir", game_dir) for x in cmdline]

    log("Command line: " + " ".join(cmdline), 90)

    import subprocess
    subprocess.call(cmdline, cwd=game_dir)

def main():
    import argparse

    parser = argparse.ArgumentParser()
    default_version = None
    if "version" in config:
        default_version = config["version"]
    parser.add_argument("username", nargs=1)
    parser.add_argument("--version", default=default_version, required=(default_version is None))
    args = parser.parse_args()
    if args.version != default_version:
        config["version"] = args.version
        _save_config()

    log("Version:  %s" % args.version)

    profile = authenticate(args.username[0])

    log("Username: %s" % profile["name"])
    log("UUID:     %s" % profile["uuid"])

    launch(profile, args.version)

if __name__ == '__main__':
    main()
