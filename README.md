

### Requirements

# Linux

For linux systems the way the app prevents screen saving when the break ui is active is by using dbus calls, for which dbus needs to be installed in the system before pip installing the python binding:

```
$ sudo apt-get install libdbus-1-dev libdbus-glib-1-dev
```

# MacOS

the app uses MacOS caffeinate command to prevent window from sleeping when break ui is active. Caffeinate is usually already installed in MacOS devices
