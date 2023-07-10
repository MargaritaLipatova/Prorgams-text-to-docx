# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:24:09 2022

@author: Vasilyeva
"""
#from tableview_SourceCodeFiles import WidgetSourceCodeFiles
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from common import *
from tableview_SourceCodeFiles import TableSourceCodeFiles
from ui_files.ui_ishod_w import Ui_DialogIshodDocx  # импорт нашего сгенерированного файла


class dialogIshodDocx(QtWidgets.QDialog):
    """ Главное диалоговое окно 'Исход-В'
    """
    def __init__(self, parent=None):
        super(dialogIshodDocx, self).__init__()
        self.ui = Ui_DialogIshodDocx()        # Инициализация ui-интерфейсов
        self.ui.setupUi(self)                 # Установка ui-интерфейсов
        self.setWindowTitle("Исход-В v.1.0")  # Название программы с версией
        self.cwd = os.getcwd()                # Получить текущее местоположение файла программы
        self.setWindowFlags(Qt.Window)        # Смена кнопок в диалговом окне вправом вехнем углу

        # Таблица "Файлы исходных кодов"
        self.formlayout = QFormLayout()
        self.ui.widget_SourceCodeFiles.setLayout(self.formlayout)
        self.tvSourceCodeFiles = TableSourceCodeFiles(self)
        self.formlayout.addRow(self.tvSourceCodeFiles)

        # Виджет с информацией о расположение сохранненого файла по кнопки "Создать документ..."
        self.ui.wStatusPathSavingDocx.setVisible(False) # скрыть информацию

        # Кнопка "Добавить файлы..."
        self.ui.pBtn_AddFilesInFolder.clicked.connect(self.btnClicked_AddFilesInFolder)

        # Кнопка "Создать документ..."
        self.ui.pBtn_CreateDocx.clicked.connect(self.btnClicked_CreateDocx)

    # def btnClicked_ChangeEx(self)-> None:
    #     """ Кнопка 'Изменить расширения...'
    #         Блокирует главное окно и открывает диалоговое окно "Изменить расширения...".
    #         Когда окно закрывают, то таблицу "Файлы исходных кодов"
    #         обновляют с учетом выбранных расширений.
    #         Returns: None
    #     """


    def btnClicked_AddFilesInFolder(self)-> None:
        """ Кнопка 'Добавить файлы...'
            Открывается диологовое окно файлового проводника.
            Returns: None
        """
        add_files = getOpenFilesAndDirs(self)
        add_files.sort()
        if add_files:
            # Подготовка списка
            listTable = set(self.tvSourceCodeFiles.getAllListTable())

            for name in add_files:
                if os.path.isdir(name):
                    scanDir_typeTableDir(listTable, name)
                else:
                    listTable.add(name)

            self.tvSourceCodeFiles.setInfoModel(listTable)

    def btnClicked_CreateDocx(self)-> None:
        """ Кнопка 'Создать документ...'
            Открывается диологовое окно файлового проводника,
            где пользователь укажет место для сохранения файла.
            Returns: None
        """
        NameDocx = self.ui.lineEdit_NameDocx.text()
        NameFile = self.ui.lineEdit_NameFile.text()

        ##!!!!!!! В стадии написания и отладки
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                            "Сохранение файла",
                            self.cwd, # Начальный путь
                            "All Files (*);;Text Files (*.txt)")

        if fileName_choose == "":
            print("\ nОтменить выбор")
            return

        # Сохранить

        print("\ nФайл, который вы выбрали для сохранения:")
        print(fileName_choose)
        print("Тип фильтра файлов:",filetype)




