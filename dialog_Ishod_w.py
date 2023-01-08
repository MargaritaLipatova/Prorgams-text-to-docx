# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:24:09 2022

@author: Vasilyeva
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

#import resources

from ui_files.ui_ishod_w import Ui_DialogIshodDocx  # импорт нашего сгенерированного файла
from dialog_ChangeExtensions import dialogChangeExtensions  
import os


class dialogIshodDocx(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(dialogIshodDocx, self).__init__()
        self.ui = Ui_DialogIshodDocx()
        self.ui.setupUi(self)
        self.cwd = os.getcwd() # Получить текущее местоположение файла программы

        
        # ------------------------------------------
        # кнопки
        # ------------------------------------------
        self.ui.pBtn_UpdateTable.setToolTip("Обновить")

        # "Изменить расширения..."
        self.ui.pBtn_ChangeEx.clicked.connect(self.btnClicked_ChangeEx)
        
        # "Добавить файлы из папки..."
        self.ui.pBtn_AddFilesInFolder.clicked.connect(self.btnClicked_AddFilesInFolder)

    def btnClicked_ChangeEx(self)-> None:
        """ Кнопка 'Изменить расширения...'
            Returns: None
        """
        _app = dialogChangeExtensions(self)
        a = _app.exec()
        print(a)
        
        
    def btnClicked_AddFilesInFolder(self)-> None:
        """ Кнопка 'Добавить файлы из папки...'
            Returns: None
        """
        dir_choose = QFileDialog.getExistingDirectory(self, "Выберите папку", self.cwd) # Начальный путь

        if dir_choose == "":
            print("\ nОтменить выбор")
            return

        print("\ nВы выбрали папку:")
        print(dir_choose)
        