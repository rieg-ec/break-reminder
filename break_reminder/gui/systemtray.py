from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QLabel, QApplication
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtGui import QIcon, QPixmap

import sys
import time
from os import path

class SystemTrayIcon(QSystemTrayIcon):

    open_settings_window_signal = pyqtSignal()
    pause_timer_signal = pyqtSignal()
    reset_timer_signal = pyqtSignal()

    break_interval_notification = 10 * 60

    def __init__(self, parent=None):
        super().__init__(parent)

        pixmap = QPixmap(path.join(path.dirname(__file__), 'assets', 'clock.png'))
        self.icon = QIcon(pixmap)
        self.setIcon(self.icon)

        self.setVisible(True)

        menu = QMenu(parent)

        self.timer = menu.addAction('00:00:00')
        self.timer.setEnabled(False)

        menu.addSeparator()

        self.pause = menu.addAction('Pause timer')
        self.pause.triggered.connect(self.pause_timer)

        self.reset = menu.addAction('Reset')
        self.reset.triggered.connect(self.reset_timer_signal.emit)

        menu.addSeparator()

        settings = menu.addAction('Settings')
        settings.triggered.connect(self.open_settings_window_signal.emit)

        menu.addSeparator()

        exitAction = menu.addAction("&Quit")
        exitAction.triggered.connect(QApplication.quit)

        self.setContextMenu(menu)

    def update_timer_countdown(self, seconds_left):
        time_clock_mode = time.strftime('%H:%M:%S', time.gmtime(seconds_left))

        self.timer.setText(time_clock_mode)

        if seconds_left:
            if seconds_left == 5 * 60:
                self.showMessage(
                    'Break Reminder',
                    '5 minutes before next break',
                    self.icon,
                    1.5 * 1000
                    )

            elif seconds_left % self.break_interval_notification == 0:
                self.showMessage('Break Reminder',
                    f'Time left until next break: {time_clock_mode}',
                    self.icon,
                    1.5 * 1000
                    )

    def pause_timer(self):
        self.pause_timer_signal.emit()
        if self.pause.text() == 'Pause timer':
            self.pause.setText('Resume timer')
        else:
            self.pause.setText('Pause timer')
