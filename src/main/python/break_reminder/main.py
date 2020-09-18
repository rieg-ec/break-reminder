from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QApplication
from gui import TransparentWindow, SystemTrayIcon, SettingsQWidget
from logic.logic import Logic
from logic.utils import ScreenSaveInhibit
import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()
    appctxt.app.setApplicationName("Break Reminder")
    appctxt.app.setQuitOnLastWindowClosed(False)

    break_window = TransparentWindow()

    system_tray_icon = SystemTrayIcon(
        appctxt.get_resource('assets'), break_window)
    config_window = SettingsQWidget()

    logic = Logic(appctxt.get_resource('config.json'))

    screen_inhibitor = ScreenSaveInhibit()
    # emitted in show() method to prevent computer from going screen save
    # mode and stop execution of break timer
    break_window.prevent_window_sleep_signal.connect(
        screen_inhibitor.inhibit_screen_saver)

    logic.display_break_ui_signal.connect(break_window.show)
    logic.hide_break_ui_signal.connect(break_window.hide)
    logic.update_timer_signal.connect(break_window.update_UI_timer)
    logic.update_timer_signal.connect(system_tray_icon.update_timer_countdown)
    logic.message_signal.connect(system_tray_icon.showMessage)

    system_tray_icon.open_settings_window_signal.connect(config_window.show)
    system_tray_icon.pause_timer_signal.connect(logic.pause)
    system_tray_icon.reset_timer_signal.connect(logic.reset)

    config_window.config_data_signal.connect(logic.update_config)

    logic.start_active()

    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
