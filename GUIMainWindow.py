import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class GUIMainWindow:
    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.central_widget = None

    def setup_window(self):
        self.main_window.setObjectName("MainWindow")
        self.main_window.resize(500, 360)
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.central_widget.setObjectName("CentralWidget")

        self.retranslate_window()

    def retranslate_window(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("GSM AT", "GSM AT"))

    def show_window(self):
        self.main_window.show()


def start_app():
    app = QtWidgets.QApplication([])
    ui = GUIMainWindow()
    ui.setup_window()
    ui.show_window()
    sys.exit(app.exec_())
