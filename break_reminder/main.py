import sys
from PyQt5.QtWidgets import QApplication

from gui import TransparentWindow
from logic import Logic

if __name__ == '__main__':
    app = QApplication([])

    window = TransparentWindow()

    logic = Logic()

    logic.display_break_ui_signal.connect(window.show)
    logic.reset_timer_signal.connect(window.startTimer)
    logic.hide_break_ui_signal.connect(window.hide)

    logic.startActiveTimer()

    sys.exit(app.exec_())
