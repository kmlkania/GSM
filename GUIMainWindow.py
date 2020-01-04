import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class GUIMainWindow:
    def __init__(self):
        self.central_widget = None

    def setup_window(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(500, 360)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("CentralWidget")

        self.retranslate_window(main_window)

    def retranslate_window(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("GSM AT", "GSM AT"))


def start_app():
    app = QtWidgets.QApplication([])
    main_window = QtWidgets.QMainWindow()
    ui = GUIMainWindow()
    ui.setup_window(main_window)
    main_window.show()
    sys.exit(app.exec_())
