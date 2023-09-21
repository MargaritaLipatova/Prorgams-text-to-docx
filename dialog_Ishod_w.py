# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:24:09 2022

@author: Vasilyeva
"""
#from tableview_SourceCodeFiles import WidgetSourceCodeFiles
import os
import subprocess

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from common import *
from convert_to_docx import Src2Docx
from tableview_SourceCodeFiles import TableSourceCodeFiles
from ui_files.ui_ishod_w import Ui_DialogIshodDocx  # импорт нашего сгенерированного файла


class Worker(QObject):
    finished = pyqtSignal()
    path = ".\\tmp_doc.docx"

    def run(self):
        """Long-running task."""
        p = subprocess.Popen(self.path, stdout=subprocess.PIPE, shell=True)
        p.wait()
        self.finished.emit()

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

        self.setWindowFlags(Qt.Window)        # Смена кнопок в диалговом окне вправом вехнем углу
        # Таблица "Файлы исходных кодов"
        self.formlayout = QFormLayout()
        self.ui.widget_SourceCodeFiles.setLayout(self.formlayout)
        self.tvSourceCodeFiles = TableSourceCodeFiles(self)
        self.formlayout.addRow(self.tvSourceCodeFiles)

        # Виджет с информацией о расположение сохранненого файла по кнопки "Создать документ..."
        self.ui.wStatusPathSavingDocx.setVisible(False) # скрыть информацию

        # Кнопка "Добавить..."

        self.ui.pBtn_AddFilesInFolder.clicked.connect(self.btnClicked_AddFilesInFolder)

        # Кнопка "Создать документ..."
        self.ui.pBtn_CreateDocx.clicked.connect(self.btnClicked_CreateDocx)

        # Кнопка "Препросмотр документа..."
        self.ui.pBnt_PreviewDocx.clicked.connect(self.btnClicked_Preview)

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

        self.create_docx(fileName_choose)
        QMessageBox.information(self, "Сохранение завершено!", "Не забудьте проверить фаил и обновить поле с количеством страниц!")

    def btnClicked_Preview(self)-> None:
        path_to_docx = os.path.join(self.cwd, "tmp_doc.docx")

        self.create_docx(path_to_docx)

       # create thread
        self.thread = QThread()
        # create object which will be moved to another thread
        self.worker = Worker()
        # move object to another thread
        self.worker.moveToThread(self.thread)
        # after that, we can connect signals from this object to slot in GUI thread
        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # start thread
        self.thread.start()

        self.setDisabled(True)

        self.thread.finished.connect(lambda: self.setDisabled(False))

    def create_docx(self, path_to_docx)-> None:
            name_doc = self.ui.lineEdit_NameFile.text().upper() #должен быть заглавными буквами, когда окажется в документе
            name_num_dec = self.ui.lineEdit_NameDocx.text()
            files = self.tvSourceCodeFiles.getDocxListTable()

            docc = Src2Docx('.\\auxiliary\\template.docx', name_doc, name_num_dec)

            docc.add_files(files)
            docc.add_koll(name_num_dec)
            docc.add_table_lri()
            docc.save_docx(path_to_docx)
