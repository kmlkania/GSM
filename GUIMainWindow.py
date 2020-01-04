import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from serialDevice import getSerialDevices


class GUIMainWindow:
    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.central_widget = None


    def setup_window(self):
        self.main_window.setObjectName("MainWindow")
        self.main_window.setGeometry(0, 0, 500, 500)
        self.main_window.setWindowTitle("GSM AT")
        self.layout = QtWidgets.QVBoxLayout()
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.central_widget.setObjectName("CentralWidget")
        self.central_widget.setGeometry(0, 0, 500, 200)
        self.ComboLbl = QtWidgets.QLabel(self.central_widget)
        self.ComboLbl.setText("moja nazwa")
        self.ComboLbl.setGeometry(10, 10, 100, 30)
        self.Combo = QtWidgets.QComboBox(self.central_widget)
        self.devices = getSerialDevices()
        self.Combo.addItems([dev.__str__() for dev in self.devices])

        self.Combo.setGeometry(10, 40, 100, 30)

        self.retranslate_window()

    def retranslate_window(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("GSM AT", "GSM AT"))
        # self.Combo.setText(_translate("MainWindow", "Select Image"))

    def show_window(self):
        self.main_window.show()


def start_app():
    app = QtWidgets.QApplication([])
    ui = GUIMainWindow()
    ui.setup_window()
    ui.show_window()
    sys.exit(app.exec_())
