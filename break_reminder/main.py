from PyQt5.QtWidgets import QApplication
from gui import TransparentWindow, SystemTrayIcon, SettingsQWidget
from logic import Logic
from logic.utils import ScreenSaveInhibit
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Break Reminder")
    app.setQuitOnLastWindowClosed(False)

    break_window = TransparentWindow()

    system_tray_icon = SystemTrayIcon(break_window)
    config_window = SettingsQWidget()

    logic = Logic()

    screen_inhibitor = ScreenSaveInhibit()
    # emitted in show() method to prevent computer from going screen save
    # mode and stop execution of break timer
    break_window.prevent_window_sleep_signal.connect(
        screen_inhibitor.inhibit_screen_saver)

    logic.display_break_ui_signal.connect(break_window.show)
    logic.hide_break_ui_signal.connect(break_window.hide)
    logic.update_timer_signal.connect(break_window.update_UI_timer)
    logic.update_timer_signal.connect(system_tray_icon.update_timer_countdown)

    system_tray_icon.open_settings_window_signal.connect(config_window.show)
    system_tray_icon.pause_timer_signal.connect(logic.pause_timer)
    system_tray_icon.reset_timer_signal.connect(logic.reset_timer)

    config_window.config_data_signal.connect(logic.update_config)

    logic.start_active_timer()

    sys.exit(app.exec_())
