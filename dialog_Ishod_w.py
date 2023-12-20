# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:24:09 2022

@author: Vasilyeva
"""
import os
import subprocess

from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QFormLayout, QMessageBox
from functools import partial
import loggers
from common import getOpenFilesAndDirs, scanDir_typeTableDir
from convert_to_docx import Src2Docx
from tableview_SourceCodeFiles import TableSourceCodeFiles
from ui_files.ui_ishod_w import \
    Ui_DialogIshodDocx  # импорт нашего сгенерированного файла


class Worker(QObject):
    finished = pyqtSignal()
    path = ".\\tmp_doc.docx"
    pid = None # id процесса
    __parent = None

    def run(self):
        """Long-running task."""
        self.__parent.create_docx(self.path)
        p = subprocess.Popen(self.path, stdout=subprocess.PIPE, shell=True)
        self.pid = p.pid
        p.wait()
        self.finished.emit()

    def get_pid(self):
        return self.pid

    def set_parent(self, parent):
        self.__parent = parent

class dialogIshodDocx(QDialog):
    """ Главное диалоговое окно 'Исход-В'
    """
    def __init__(self, parent=None):
        super(dialogIshodDocx, self).__init__()

        try:
            self.loggers = loggers.get_logger(dialogIshodDocx.__name__)
            self.loggers.info('start')
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

            # Виджет с информацией о расположении сохранненого файла по кнопки "Создать документ..."
            self.ui.wStatusPathSavingDocx.setVisible(False) # скрыть информацию

            # Кнопка "Добавить..."
            self.ui.pBtn_AddFilesInFolder.clicked.connect(self.btnClicked_AddFilesInFolder)

            # Кнопка "Создать документ..."
            self.ui.pBtn_CreateDocx.clicked.connect(self.btnClicked_CreateDocx)

            # Кнопка "Препросмотр документа..."
            self.ui.pBnt_PreviewDocx.clicked.connect(self.btnClicked_Preview)
            self.loggers.info('end')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def btnClicked_AddFilesInFolder(self)-> None:
        """ Кнопка 'Добавить файлы...'
            Открывается диологовое окно файлового проводника.
            Returns: None
        """
        try:
            self.loggers.info('start')
            add_files = getOpenFilesAndDirs(self) # Выбор файлов и/или папок
            add_files.sort()

            if add_files:
                # Ранее добавленные файлы в таблицу
                listTable:set = self.tvSourceCodeFiles.getAllListTable()

                # Подготовка списка файлов
                for name in add_files:
                    if os.path.isdir(name):
                        scanDir_typeTableDir(listTable, name)
                    else:
                        listTable.add(name)

                # Добавление файлов в таблицу
                self.tvSourceCodeFiles.setInfoModel(listTable)

            self.loggers.info('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def btnClicked_CreateDocx(self)-> None:
        """ Кнопка 'Создать документ...'
            Открывается диологовое окно файлового проводника,
            где пользователь укажет место для сохранения файла.
            Returns: None
        """
        try:
            self.loggers.info('start')
            NameDocx = self.ui.lineEdit_NameDocx.text()
            # NameFile = self.ui.lineEdit_NameFile.text()
            default_filename = os.path.join(self.cwd, NameDocx)

            ##!!!!!!! В стадии написания и отладки
            fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                            "Сохранение файла",
                                            default_filename, # Начальный путь
                                            "Text Files (*.docx)"
                                            )

            if fileName_choose == "":
                self.loggers.info("\ nОтменить выбор")
            else:
                # Сохранить

                self.loggers.info("\ nФайл, который вы выбрали для сохранения:")
                self.loggers.info(fileName_choose)
                self.loggers.info(f"Тип фильтра файлов: {filetype}")

                self.create_docx(fileName_choose)
                QMessageBox.information(self, "Сохранение завершено!", "Не забудьте проверить фаил и обновить поле с количеством страниц!")

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def btnClicked_Preview(self)-> None:
        """ Кнопка 'Предпросмотр...'
            Открывается файл для сохранения.
        """
        try:
            self.loggers.info('start')
            # create thread
            self.thread = QThread()
            # create object which will be moved to another thread
            self.worker = Worker()
            self.worker.set_parent(self)
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
            self.thread.finished.connect(partial(self.setDisabled, False))

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def create_docx(self, path_to_docx)-> None:
        """ Создание/сохранение файла
        Args:
            path_to_docx (_type_): путь к файлу
        """
        try:
            self.loggers.info('start')
            name_doc = self.ui.lineEdit_NameFile.text().upper() #должен быть заглавными буквами, когда окажется в документе
            name_num_dec = self.ui.lineEdit_NameDocx.text().upper()
            files = self.tvSourceCodeFiles.getDocxListTable()

            docc = Src2Docx('.\\auxiliary\\template.docx', name_doc, name_num_dec)

            docc.add_files(files)
            docc.add_koll(name_num_dec)
            docc.add_table_lri()
            docc.save_docx(path_to_docx)
            self.loggers.info('end')
        except Exception as err:
            self.loggers.warning(f'Exception = {err}')
