from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from pynput import keyboard
import time
import threading


class Logic(QObject):

    display_break_ui_signal = pyqtSignal(int)
    reset_timer_signal = pyqtSignal(int)
    hide_break_ui_signal = pyqtSignal()

    class CountDown(QObject):
        end_break_signal = pyqtSignal()
        end_active_signal = pyqtSignal()

        def __init__(self):
            super().__init__()
            self.time_left = None

        def startAsBreakCounter(self, time):
            self.is_break = True
            self.time_left = time

        def startAsActiveCounter(self, time):
            self.is_break = False
            self.time_left = time

        def updateTime(self):
            if not self.time_left:
                if self.is_break:
                    self.end_break_signal.emit()
                    self.is_break = False
                else:
                    self.end_active_signal.emit()
                    self.is_break = True

            else:
                print('time left:', self.time_left, self.is_break)
                self.time_left -= 1

        def reset(self, time_left):
            # add 1 to prevent finishing before visual timer gets to 00:00
            self.time_left = time_left + 1

    # TODO: move to a json config file
    break_time = 60 * 8
    active_time = 60 * 40

    def __init__(self):
        super().__init__()

        self.counter = self.CountDown()
        self.counter.end_active_signal.connect(self.startBreakTimer)
        self.counter.end_break_signal.connect(self.startActiveTimer)

        self.timer = QTimer(self)
        self.timer.setInterval(1 * 1000)
        self.timer.timeout.connect(self.counter.updateTime)
        self.timer.start()

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def startActiveTimer(self, time=active_time):
        self.counter.startAsActiveCounter(time)
        self.hide_break_ui_signal.emit()

    def startBreakTimer(self, time=break_time):
        self.counter.startAsBreakCounter(time)
        self.display_break_ui_signal.emit(time)


    def on_press(self, key):
        ''' key listener method '''
        if self.counter.is_break:
            if key == keyboard.Key.esc:
                self.startActiveTimer()

            elif key == keyboard.Key.f1:
                # TODO: move constants to json file
                self.startActiveTimer(60 * 5)

            else:
                # reset break timer:
                self.reset_timer_signal.emit(self.break_time)
                self.counter.reset(self.break_time)
