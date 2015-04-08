#!/usr/bin/env python3

def log(msg, color=36):
    print(u"\u001b[" + str(color) + "m\u001b[1m" + msg + u"\u001b[0m")
