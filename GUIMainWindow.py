import sys
from PyQt5 import QtWidgets
from GUIWidgets import GUIWidget


class GUIMainWindow:
    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.gui_widget = GUIWidget(self.main_window)
        self.main_window_elements = {}

    def setup_window(self):
        self.setup_main_window()
        self.main_window_elements['head_widget'] = self.gui_widget.setup_head_widget()
        self.main_window_elements['bottom_widget'] = self.gui_widget.setup_bottom_widget()
        self.main_window_elements['footer_widget'] = self.gui_widget.setup_footer_widget()
        self.gui_widget.setup_actions()

    def setup_main_window(self):
        self.main_window.setObjectName("MainWindow")
        self.main_window.setGeometry(0, 0, 550, 550)
        self.main_window.setWindowTitle("GSM AT")

    def show_window(self):
        self.main_window.show()


def start_app():
    app = QtWidgets.QApplication(sys.argv)
    ui = GUIMainWindow()
    ui.setup_window()
    ui.show_window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()
