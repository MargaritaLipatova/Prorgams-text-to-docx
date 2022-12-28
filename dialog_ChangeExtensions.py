# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:49:35 2022

@author: Vasilyeva
"""

from PyQt5 import QtWidgets
from ui_dialogChangeExtensions import Ui_dialogChangeExtensions # импорт нашего сгенерированного файла


class dialogChangeExtensions(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(dialogChangeExtensions, self).__init__(parent, QtWidgets.QDialog)#QtCore.Qt.Window)
        self.ui = Ui_dialogChangeExtensions()
        self.ui.setupUi(self)
         