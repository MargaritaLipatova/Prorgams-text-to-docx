# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:24:09 2022

@author: Vasilyeva
"""
from PyQt5 import QtWidgets
from ui_ishod_w import Ui_DialogIshodDocx  # импорт нашего сгенерированного файла
from dialog_ChangeExtensions import dialogChangeExtensions  
#import sys


class dialogIshodDocx(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(dialogIshodDocx, self).__init__()
        self.ui = Ui_DialogIshodDocx()
        self.ui.setupUi(self)
    
        # ------------------------------------------
        # кнопки
        # ------------------------------------------

        # подключение клик-сигнал к слоту btnClicked
        self.ui.pBtn_ChangeEx.clicked.connect(self.btnClicked_ChangeEx)

    def btnClicked_ChangeEx(self)-> None:
        """ Кнопка 'Изменить расширения...'
            Returns: None
        """
        _app = dialogChangeExtensions(parent=self)
        _app.show()
        a = _app.exec()
        print(a)
        