from PyQt5.QtWidgets import QApplication
from gui import TransparentWindow, SystemTrayIcon, SettingsQWidget
from logic import Logic
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Break Reminder")
    app.setQuitOnLastWindowClosed(False)

    window = TransparentWindow()
    system_tray_icon = SystemTrayIcon(window)
    config_window = SettingsQWidget()

    logic = Logic()

    logic.display_break_ui_signal.connect(window.show)
    logic.hide_break_ui_signal.connect(window.hide)
    logic.update_timer_signal.connect(window.update_UI_timer)
    logic.update_timer_signal.connect(system_tray_icon.update_timer_countdown)

    system_tray_icon.open_settings_window_signal.connect(config_window.show)
    system_tray_icon.pause_timer_signal.connect(logic.pause_timer)
    system_tray_icon.reset_timer_signal.connect(logic.reset_timer)

    config_window.config_data_signal.connect(logic.update_config)

    logic.start_active_timer()

    sys.exit(app.exec_())
