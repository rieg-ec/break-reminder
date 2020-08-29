from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QApplication)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QVBoxLayout

import time

class TransparentWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.update_label_timer = QTimer(self)
        self.update_label_timer.setInterval(1 * 1000)
        self.update_label_timer.timeout.connect(self.updateUITimer)

    def initUI(self):
        '''
        WindowStaysOnTopHint for always on top,
        WindowTransparentForInput makes QWidget frameless,
        FramelessWindowHint makes transparent for input
        '''

        layout = QVBoxLayout()

        ### TIMER LABEL ###
        self.timer_label = QLabel('', self)
        self.timer_label.setStyleSheet('font-size: 50px;')
        self.timer_label.setAlignment(Qt.AlignCenter)
        ###################

        ### INSTRUCTIONS LABELS ###
        instructions_vbox = QVBoxLayout()

        instructions_label_1 = QLabel("Press 'Esc' to stop break", self)
        instructions_label_1.setStyleSheet('font-size: 30px;')

        instructions_label_2 = QLabel(
            "Press 'F1' to be active 5 more minutes", self)
        instructions_label_2.setStyleSheet('font-size: 30px;')

        instructions_vbox.addWidget(instructions_label_1)
        instructions_vbox.addStretch(1)
        instructions_vbox.addWidget(instructions_label_2)

        ###########################

        layout.insertStretch(0, stretch=3)
        layout.addWidget(self.timer_label)
        layout.insertStretch(2, stretch=1)
        layout.addLayout(instructions_vbox)
        layout.insertStretch(4, stretch=3)

        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # TODO: Qt.X11BypassWindowManagerHint
        self.setWindowFlags(self.windowFlags() |
            Qt.WindowStaysOnTopHint |
            Qt.WindowTransparentForInput |
            Qt.FramelessWindowHint)

        # adjust transparency (opacity):
        self.setWindowOpacity(0.5)
        # full screen:
        self.resize(QApplication.desktop().size())
        # self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet(
            'background-color: black;'
           +'color: white;')

    def show(self, time):
        super().show()
        self.startTimer(time)

    def hide(self):
        ''' called when break cronometer ends '''
        super().hide()

    def startTimer(self, time):
        ''' called to start/reset cronometer '''
        self.time_left = time
        self.update_label_timer.start()

    def updateUITimer(self):
        ''' called to update cronometer ui countdown '''
        if self.time_left:
            self.time_left -= 1
            current_time = time.strftime('%M:%S', time.gmtime(self.time_left))
            self.timer_label.setText(current_time)
