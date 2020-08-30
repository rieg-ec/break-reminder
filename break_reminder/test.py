import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon

from gui import TransparentWindow
from logic import Logic

break_time = 5
active_time = 10
prolong_break = 5

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Break Reminder")
    app.setQuitOnLastWindowClosed(False)

    window = TransparentWindow()
    logic = Logic(break_time, active_time, prolong_break)

    logic.display_break_ui_signal.connect(window.show)
    logic.reset_timer_signal.connect(window.startTimer)
    logic.hide_break_ui_signal.connect(window.hide)

    logic.startActiveTimer()

    sys.exit(app.exec_())
