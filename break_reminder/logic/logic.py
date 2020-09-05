from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from pynput import keyboard
from os import path
import json
import threading

from logic.utils import json_hook

class Logic(QObject):

    class CountDown(QObject):
        end_break_signal = pyqtSignal()
        end_active_signal = pyqtSignal()

        clock_counter_signal = pyqtSignal(int)

        prolong_break = 5 * 60

        def __init__(self):
            super().__init__()
            self.update_attrs_from_config()
            self.tick = 1

        def update_attrs_from_config(self):
            with open(path.join(path.dirname(__file__),
                    'config.json'), 'r') as file:

                parameters = json.loads(file.read(), object_hook=json_hook)
                self.break_time = parameters['break_time']
                self.active_time = parameters['active_time']

        def start_as_break_counter(self):
            self.is_break = True
            self.time_left = self.break_time

        def start_as_active_counter(self, prolong_break=False):
            self.is_break = False
            if prolong_break:
                self.time_left = self.prolong_break
            else:
                self.time_left = self.active_time

        def pause(self):
            if self.tick:
                self.tick = 0
            else:
                self.tick = 1

        def updateTime(self):
            if not self.time_left:
                if self.is_break:
                    self.end_break_signal.emit()
                    self.is_break = False
                else:
                    self.end_active_signal.emit()
                    self.is_break = True

            else:
                self.time_left -= self.tick # 1 or 0 if pause
                self.clock_counter_signal.emit(self.time_left)

    display_break_ui_signal = pyqtSignal(int)
    hide_break_ui_signal = pyqtSignal()
    # signal to update all ui clocks in real time:
    update_timer_signal = pyqtSignal(int)

    lock = threading.Lock()

    def __init__(self):
        super().__init__()
        self.counter = self.CountDown()
        self.counter.end_active_signal.connect(self.start_break_timer)
        self.counter.end_break_signal.connect(self.start_active_timer)
        self.counter.clock_counter_signal.connect(
            self.update_timer_signal.emit)

        self.timer = QTimer(self)
        self.timer.setInterval(1 * 1000)
        self.timer.timeout.connect(self.counter.updateTime)
        self.timer.start()

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def start_active_timer(self, prolong_break=False):
        self.counter.start_as_active_counter(prolong_break=prolong_break)
        self.hide_break_ui_signal.emit()

    def start_break_timer(self):
        self.counter.start_as_break_counter()
        self.display_break_ui_signal.emit(self.counter.time_left)

    def pause_timer(self):
        self.counter.pause()

    def reset_timer(self):
        self.hide_break_ui_signal.emit()
        self.counter.start_as_active_counter()

    def on_press(self, key):
        ''' key listener method '''
        if self.counter.is_break:
            if key == keyboard.Key.esc:
                self.start_active_timer()

            elif key == keyboard.Key.f1:
                self.start_active_timer(prolong_break=True)

            else:
                self.counter.start_as_break_counter()

    def update_config(self, config):
        self.update_config_thread = threading.Thread(
            target=self.update_config_from_thread,
            args=[config])

        self.update_config_thread.start()

    def update_config_from_thread(self, config):
        with self.lock:
            with open(path.join(path.dirname(__file__),
                    'config.json'), 'r+') as file:

                parameters = json.loads(file.read(), object_hook=json_hook)
                file.seek(0)
                for key, value in config.items():
                    parameters[key] = value
                file.write(json.dumps(parameters))
                file.truncate()
            # update counter attributes from new config file:
            self.counter.update_attrs_from_config()
