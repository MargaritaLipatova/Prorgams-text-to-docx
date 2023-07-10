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
import subprocess

from common import *
from convert_to_docx import Src2Docx
from dialog_ChangeExtensions import dialogChangeExtensions
from tableview_SourceCodeFiles import TableSourceCodeFiles
from ui_files.ui_ishod_w import \
    Ui_DialogIshodDocx  # импорт нашего сгенерированного файла


class dialogIshodDocx(QtWidgets.QDialog):
    """ Главное диалоговое окно 'Исход-В'
    """
    def __init__(self, parent=None):
        super(dialogIshodDocx, self).__init__()
        self.ui = Ui_DialogIshodDocx()        # Инициализация ui-интерфейсов
        self.ui.setupUi(self)                 # Установка ui-интерфейсов
        self.setWindowTitle("Исход-В v.1.0")  # Название программы с версией
        self.cwd = os.getcwd()                # Получить текущее местоположение файла программы

        # Таблица "Файлы исходных кодов"
        formlayout = QFormLayout()
        self.ui.widget_SourceCodeFiles.setLayout(formlayout)
        self.tvSourceCodeFiles = TableSourceCodeFiles(self)
        self.formlayout.addRow(self.tvSourceCodeFiles)

        # Виджет с информацией о расширениях
        self.ui.wStatusExtensions.setVisible(False)  # скрыть информацию
        self.ui.pBtn_ChangeEx.setEnabled(False)      # неактивная кнопка ,т.к. пуста таблица "Файлы исходных кодов"

        # Виджет с информацией о расположение сохранненого файла по кнопки "Создать документ..."
        self.ui.wStatusPathSavingDocx.setVisible(False) # скрыть информацию

        # Кнопка "Обновить таблицу"
        self.ui.pBtn_UpdateTable.setToolTip("Обновить") # подсказака, текст появляется при наведение стрелки мыши

        # Кнопка "Изменить расширения..."
        self.ui.pBtn_ChangeEx.clicked.connect(self.btnClicked_ChangeEx)

        # Кнопка "Добавить файлы..."
        self.ui.pBtn_AddFilesInFolder.clicked.connect(self.btnClicked_AddFilesInFolder)

        # Кнопка "Создать документ..."
        self.ui.pBtn_CreateDocx.clicked.connect(self.btnClicked_CreateDocx)

        # Кнопка "Препросмотр документа..."
        self.ui.pBnt_PreviewDocx.clicked.connect(self.btnClicked_Preview)

    def btnClicked_ChangeEx(self)-> None:
        """ Кнопка 'Изменить расширения...'
            Блокирует главное окно и открывает диалоговое окно "Изменить расширения...".
            Когда окно закрывают, то таблицу "Файлы исходных кодов"
            обновляют с учетом выбранных расширений.
            Returns: None
        """
        _app = dialogChangeExtensions(self)
        a = _app.exec()
        print(a)


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

            for name in add_files:    # Проход по выделенному списку
                if os.path.isdir(name):
                        if self.ui.checkBox_FolderNesting.isChecked():
                            scanDir_typeTableDir(listTable, name)
                else:
                    listTable.add(name)

            self.tvSourceCodeFiles.setInfoModel(listTable)
            print("*******************************************")
            print(self.tvSourceCodeFiles.getDocxListTable())
            print("*******************************************")

    def btnClicked_CreateDocx(self)-> None:
        """ Кнопка 'Создать документ...'
            Открывается диологовое окно файлового проводника,
            где пользователь укажет место для сохранения файла.
            Returns: None
        """
        ##!!!!!!! В стадии написания и отладки
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                            "Сохранение файла",
                            self.cwd, # Начальный путь
                            "All Files (*);;Text Files (*.docx)")

        if fileName_choose == "":
            print("\ nОтменить выбор")
            return

        # Сохранить

        print("\ nФайл, который вы выбрали для сохранения:")
        print(fileName_choose)
        print("Тип фильтра файлов:",filetype)

        self.create_docx(fileName_choose)
        QMessageBox.information(self, "Сохранение завершено!", "Не забудьте проверить фаил и обновить поле с количеством страниц!")

    def btnClicked_Preview(self)-> None:
        path_to_docx = os.path.join(self.cwd, "tmp_doc.docx")

        self.create_docx(path_to_docx)

        p = subprocess.Popen(path_to_docx, stdout=subprocess.PIPE, shell=True)

        p.wait()

    def create_docx(self, path_to_docx)-> None:
            name_doc = self.ui.lineEdit_NameFile.text() #должен быть заглавными буквами, когда окажется в документе
            name_num_dec = self.ui.lineEdit_NameDocx.text()
            files = self.tvSourceCodeFiles.getDocxListTable()

            docc = Src2Docx('.\\template.docx', name_doc, name_num_dec)

            docc.add_files(files)
            docc.add_koll(name_num_dec)
            docc.add_table_lri()
            docc.save_docx(path_to_docx)