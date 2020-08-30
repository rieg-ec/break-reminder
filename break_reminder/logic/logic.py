from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from pynput import keyboard

class Logic(QObject):

    class CountDown(QObject):
        end_break_signal = pyqtSignal()
        end_active_signal = pyqtSignal()

        clock_counter_signal = pyqtSignal(int)

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
                self.clock_counter_signal.emit(self.time_left)

        def reset(self, time_left):
            # add 1 to prevent finishing before visual timer gets to 00:00
            self.time_left = time_left + 1

    display_break_ui_signal = pyqtSignal(int)
    hide_break_ui_signal = pyqtSignal()
    # signal to update all ui clocks in real time:
    update_timer_signal = pyqtSignal(int)

    def __init__(self, break_time, active_time, prolong_break):
        super().__init__()
        self.break_time = break_time
        self.active_time = active_time
        self.prolong_break = prolong_break

        self.counter = self.CountDown()
        self.counter.end_active_signal.connect(self.startBreakTimer)
        self.counter.end_break_signal.connect(self.startActiveTimer)
        self.counter.clock_counter_signal.connect(
            self.update_timer_signal.emit)

        self.timer = QTimer(self)
        self.timer.setInterval(1 * 1000)
        self.timer.timeout.connect(self.counter.updateTime)
        self.timer.start()

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def startActiveTimer(self, time=None):
        if time is None:
            time = self.active_time

        self.counter.startAsActiveCounter(time)
        self.hide_break_ui_signal.emit()

    def startBreakTimer(self, time=None):
        if time is None:
            time = self.break_time

        self.counter.startAsBreakCounter(time)
        self.display_break_ui_signal.emit(time)


    def on_press(self, key):
        ''' key listener method '''
        if self.counter.is_break:
            if key == keyboard.Key.esc:
                self.startActiveTimer()

            elif key == keyboard.Key.f1:
                self.startActiveTimer(self.prolong_break)

            else:
                self.counter.reset(self.break_time)
