mcl
===

Python minecraft launcher

This launcher cannot currently download new versions but it can log in.

Usage
-----

```
./launcher.py --version <version> <username>
```

The version is only required on first launch, it will be saved in the config file for future use.

When the authentication is found to be invalid or you didn't log in with that account before, a password will be requested through either console or tkinter depending on your environment.

Config
------

Data is stored in `~/.config/mcl.json`.
