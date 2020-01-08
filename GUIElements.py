from PyQt5 import QtWidgets


class GUIElements:
    @classmethod
    def add_lbl(cls, widget, geometry, text=''):
        lbl = QtWidgets.QLabel(widget)
        lbl.setGeometry(geometry)
        lbl.setText(text)
        return lbl

    @classmethod
    def add_push_btn(cls, widget, geometry, name='', text=''):
        btn = QtWidgets.QPushButton(widget)
        btn.setGeometry(geometry)
        btn.setObjectName(name)
        btn.setText(text)
        return btn

    @classmethod
    def add_combo_box(cls, widget, geometry, items=(), name=''):
        combo = QtWidgets.QComboBox(widget)
        combo.addItems(items)
        combo.setGeometry(geometry)
        combo.setObjectName(name)
        return combo

    @classmethod
    def add_line_edit(cls, widget, geometry, name=''):
        line = QtWidgets.QLineEdit(widget)
        line.setGeometry(geometry)
        line.setObjectName(name)
        return line

    @classmethod
    def add_list_w(cls, widget, geometry, selection_mode, name=''):
        list_w = QtWidgets.QListWidget(widget)
        list_w.setGeometry(geometry)
        list_w.setSelectionMode(selection_mode)
        list_w.setObjectName(name)
        return list_w
