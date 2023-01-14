# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:49:35 2022

@author: Vasilyeva
"""

from PyQt5 import QtWidgets
from ui_files.ui_dialogChangeExtensions import Ui_dialogChangeExtensions # импорт нашего сгенерированного файла


class dialogChangeExtensions(QtWidgets.QDialog, Ui_dialogChangeExtensions):
    """ Диалоговое окно 'Изменить расширения...'.
        Отображает расширения всех файлов 
        находящихся в таблице "Файлы исходных кодов".
        Перед каждым расширением есть checkBox
        Если галочка установлена, то файл с этим расширением будет 
        отображаться в таблице, иначе будет скрыт.
    """
    def __init__(self, parent=None, filterEx=[]):
       ##!!!!!!! В стадии написания и отладки
        super(dialogChangeExtensions, self).__init__(parent)
        self.ui = Ui_dialogChangeExtensions()
        self.ui.setupUi(self)
#        self.setupUi(self)
        # "Изменить расширения..."
        self.ui.pushButton_Ok.clicked.connect(self.btnClicked_Ok)
        
        # "Добавить файлы из папки..."
        self.ui.pushButton_Cancel.clicked.connect(self.btnClicked_Cancel)
        
    def btnClicked_Ok(self)-> None:
        """ Кнопка 'Ok'
            Returns: None
        """
        self.accept()
    
    def btnClicked_Cancel(self)-> None:
        """ Кнопка 'Отмена'
            Returns: None
        """
        self.reject()
    