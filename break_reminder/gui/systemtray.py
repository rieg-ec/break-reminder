from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QLabel
import sys
import time

# TODO: add qline edits to make ui prettier

class SystemTrayIcon(QSystemTrayIcon):

    break_interval_notification = 10 # minutes

    def __init__(self, parent=None):
        super().__init__(parent)
        # TODO: set icon
        # self.icon = None
        # self.setIcon(self.icon)
        menu = QMenu(parent)
        menu.setTitle("Break Reminder")

        self.timer_label = QLabel('<b>Hola</b>')
        menu.setDefaultWidget(self.timer_label)

        exitAction = menu.addAction("Quit")
        # TODO: is this the best way to exit app?
        exitAction.triggered.connect(sys.exit)

        self.setContextMenu(menu)

        self.show()

        # TODO: is this useful at all?
        self.setToolTip("tool tip")

    def updateTimerCountdown(self, seconds_left):
        self.timer_label = time.strftime(
            '%M:%S', time.gmtime(seconds_left))

        if seconds_left % (60 * self.break_interval_notification) == 0:
            self.showMessage('Break Reminder',
                            f'Time left until next break: {time}')
