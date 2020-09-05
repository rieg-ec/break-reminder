import json
import shlex, subprocess
import platform
import time
import threading

def json_hook(dict_):
    """
    object_hook to convert values to integer
    """
    if isinstance(dict_, str):
        try:
            return int(dict_)
        except ValueError:
            return dict_
    elif isinstance(dict_, dict):
        return {k: json_hook(v) for k, v in dict_.items()}
    elif isinstance(dict_, list):
        return [json_hook(v) for v in dict_]
    else:
        return dict_


class ScreenSaveInhibit:
    ''' made to be executed in separated thread to prevent
    screen from sleeping
    '''
    def __init__(self):
        self.system = platform.system()

    def inhibit_screen_saver(self, seconds):
        seconds += 120 # prevent instant sleeping after breaks
        if self.system == 'Linux':
            th = threading.Thread(
                target=self.prevent_screensaver_linux,
                args=[seconds],
                daemon=True)

            th.start()

        elif self.system == 'Darwin':
            self.prevent_screensaver_macos(seconds)

        elif self.system == 'Windows':
            pass

    def prevent_screensaver_macos(self, seconds):
        command_line = f'caffeinate -u -t {seconds}'
        subprocess.Popen(shlex.split(command_line))

    def prevent_screensaver_windows(self, seconds):
        # windows way of preventing idle sleep:
        # ctypes.windll.kernel32.SetThreadExecutionState('0x80000002')
        pass

    def prevent_screensaver_linux(self, seconds):
        '''
        inhibits screen saver for {seconds} and sleeps {seconds}
        before uninhibit
        '''
        import dbus

        bus = dbus.SessionBus()
        saver = bus.get_object('org.freedesktop.ScreenSaver', '/ScreenSaver')
        saver_interface = dbus.Interface(saver,
            dbus_interface='org.freedesktop.ScreenSaver')
        # now we can inhibit the screensaver
        try:
            cookie = saver_interface.Inhibit("break reminder", "ux reasons")
            # adds 2 minutes to prevent instant sleeping after break ends
            time.sleep(seconds)
            success = True

        except Exception as error:
            success = False

        finally:
            if success:
                saver_interface.UnInhibit(cookie)
