### Minimalist break reminder app written in Python/Qt made for personal use to manage breaks from screen time :computer: :clock4:
---
### Requirements:

# Linux

The way the app prevents screen saving when the break ui is active is by using dbus calls, for which dbus package needs to be installed in the system before pip installing the python binding:

```
$ sudo apt-get install libdbus-1-dev libdbus-glib-1-dev
```
This method should work in KDE and Gnome desktops (older versions may not be supported).

# MacOS

The app uses MacOS caffeinate command to prevent window from sleeping when break ui is active. Caffeinate should already be installed in MacOS devices (tested in Catalina).
