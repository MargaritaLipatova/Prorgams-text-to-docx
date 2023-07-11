# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:49:35 2022

@author: Vasilyeva
"""

from PyQt5 import QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui_files.ui_dialogChangeExtensions import Ui_dialogChangeExtensions # импорт нашего сгенерированного файла


class dialogChangeExtensions(QDialog, Ui_dialogChangeExtensions):
    """ Диалоговое окно 'Изменить расширения...'.
        Отображает расширения всех файлов
        находящихся в таблице "Файлы исходных кодов".
        Перед каждым расширением есть checkBox
        Если галочка установлена, то файл с этим расширением будет
        отображаться в таблице, иначе будет скрыт.
    """
    def __init__(self, parent=None, filterEx=[]):
        super(dialogChangeExtensions, self).__init__(parent)
        self.ui = Ui_dialogChangeExtensions()        # Инициализация ui-интерфейсов
        self.ui.setupUi(self)                 # Установка ui-интерфейсов
        self.ui.pBtn_Ok.clicked.connect(self.btnClicked_Ok)            # "Изменить расширения..."
        self.ui.pBtn_Cancel.clicked.connect(self.btnClicked_Cancel)    # "Добавить файлы из папки..."
        self._is_filter = False

    @property
    def is_filter(self):
        return self._is_filter

    @is_filter.setter
    def is_filter(self, state):
        self._is_filter = state

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


    def set_Filter_ex(self, filters):
        for filter in filters:
            newItem = QListWidgetItem(self)
            newItem.setText(filter)
            self.listWidget_Extensions.insertItem(self.listWidget_Extensions.rowCount(), newItem)

