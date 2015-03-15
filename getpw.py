#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

def _console(title, msg):
    import getpass
    return getpass.getpass(msg)

def _gui(title, msg):
    import tkinter
    import tkinter.simpledialog
    _frame = tkinter.Frame()
    _frame.master.geometry("1x1+1+1")
    _frame.master.attributes("-type", "dock")
    _frame.master.attributes("-topmost", "true")
    repl = tkinter.simpledialog.askstring(title, msg)
    _frame.master.destroy()
    if not repl:
        raise Exception("No password entered")
    return repl

import os
import sys

if os.isatty(sys.stdin.fileno()):
    getpw = _console
else:
    getpw = _gui
