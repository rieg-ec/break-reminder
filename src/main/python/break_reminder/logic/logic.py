from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from pynput import keyboard
import json
import threading

from .utils import json_hook


class Logic(QObject):

    display_break_ui_signal = pyqtSignal(int)
    hide_break_ui_signal = pyqtSignal()
    # signal to update all ui clocks in real time:
    update_timer_signal = pyqtSignal(int)
    # signal to pop notification at active intervals:
    message_signal = pyqtSignal(int)

    PROLONG_BREAK = 5 * 60

    lock = threading.Lock()

    def __init__(self, config_file_path):
        super().__init__()
        self.config_file_path = config_file_path

        self.update_attrs()
        self.tick = 1

        self.timer = QTimer(self)
        self.timer.setInterval(1 * 1000)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def start_active(self, prolong_break=False):
        self.is_break = False
        if prolong_break:
            self.time_left = self.PROLONG_BREAK
        else:
            self.time_left = self.active_time

        self.hide_break_ui_signal.emit()

    def start_break(self):
        self.is_break = True
        self.time_left = self.break_time

        self.display_break_ui_signal.emit(self.time_left)

    def pause(self):
        self.tick = 0 if self.tick else 1

    def reset(self):
        if self.is_break:
            self.time_left = self.break_time
        else:
            self.time_left = self.active_time

    def update_time(self):
        if not self.time_left:
            if self.is_break:
                self.start_active()
            else:
                self.start_break()

        else:
            self.time_left -= self.tick  # 1 or 0 if pause
            self.update_timer_signal.emit(self.time_left)

            if self.send_message and self.time_left:
                if self.time_left == 5 * 60 or\
                self.time_left % self.notification_interval == 0:
                    self.message_signal.emit(self.time_left)

    def on_press(self, key):
        ''' key listener method '''
        if self.is_break:
            if key == keyboard.Key.esc:
                self.start_active()

            elif key == keyboard.Key.f1:
                self.start_active(prolong_break=True)

            else:
                self.start_break()

    def update_config(self, config):
        update_config_thread = threading.Thread(
            target=self.__update_config_from_thread,
            args=[config])

        update_config_thread.start()

    def __update_config_from_thread(self, config):
        with self.lock:
            with open(self.config_file_path, 'r+') as file:
                parameters = json.loads(file.read(), object_hook=json_hook)
                file.seek(0)
                for key, value in config.items():
                    parameters[key] = value
                file.write(json.dumps(parameters))
                file.truncate()
        # update class attributes associated with config file:
        for key, value in parameters.items():
            if not isinstance(value, list):
                setattr(self, key, value)
        self.send_message = parameters['notification_interval'][0]
        self.notification_interval = parameters['notification_interval'][1]

    def update_attrs(self):
        update_attrs_thread = threading.Thread(
            target=self.__update_attrs_from_thread)
        update_attrs_thread.start()

    def __update_attrs_from_thread(self):
        with self.lock:
            with open(self.config_file_path, 'r') as file:
                parameters = json.loads(file.read(), object_hook=json_hook)
                for key, value in parameters.items():
                    if not isinstance(value, list):
                        setattr(self, key, value)
                self.send_message = parameters['notification_interval'][0]
                self.notification_interval = parameters[
                    'notification_interval'][1]
