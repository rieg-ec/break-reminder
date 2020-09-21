### Minimalist break reminder app written in Python/Qt made for personal use to manage breaks from screen time :computer: :clock4:
---
### Requirements:



**Python**:
fbs doesn't support python 3.7+, therefore python3.6 or python3.5 must be used.

**Linux**:
The app has only been tested in linux os (Ubuntu 18.04). MacOS will be supported soon.

The way the app prevents screen saving when the break ui is active is by using dbus calls, for which dbus package needs to be installed in the system before pip installing the python binding:

```
$ sudo apt install libdbus-1-dev libdbus-glib-1-dev
```
This method should work in KDE and Gnome desktops (older versions may not be supported).

---
### How to use:

once requirements have been installed, there are three ways to run the app:

### Linux:

1. ```fbs run``` within the top directory to run from terminal

2. ```fbs freeze``` to freeze the app, this will create a folder called ```target``` containing the app folder. ```cd``` into it and run ``` ./Break-Reminder/Break-Reminder``` to launch the app

3. ```fbs installer``` (fpm must be installed. If not, run ```sudo apt install ruby ruby-dev rubygems build-essential``` and then  ```sudo gem install --no-document fpm```) .This will create a .deb file to install the app.

#### Known errors:

1. "Error! You probably have to install the development version of Python package"
``` sudo apt install python3-dev ```
2. If changing the timers hour/minutes does not work, it may be due to write permissions in config.json. Try rebooting and if that does not work, run ```sudo chmod 766 config.json``` inside the app folder.
