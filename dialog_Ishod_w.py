# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:24:09 2022

@author: Vasilyeva
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui_files.ui_ishod_w import Ui_DialogIshodDocx  # импорт нашего сгенерированного файла
from dialog_ChangeExtensions import dialogChangeExtensions  
from tableview_SourceCodeFiles import TableSourceCodeFiles  
from common import *
#from tableview_SourceCodeFiles import WidgetSourceCodeFiles  
import os

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
        self.formlayout = QFormLayout()
        self.ui.widget_SourceCodeFiles.setLayout(self.formlayout)
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
        selected_files = getOpenFilesAndDirs(self)
        selected_files.sort()
        if selected_files:
                
            # Подготовка списка 
            PathsDir     = self.tvSourceCodeFiles.getPathsDir()
            saveTableDir = self.tvSourceCodeFiles.getTableDir()
            dirSelection = selected_files[0].split("/" + selected_files[0].split("/")[-1])[0]


            if dirSelection not in PathsDir:
                # Папки с таким названием ещё не было
                dir1 = tableDir(dirSelection)
                saveTableDir.append(dir1)
            else:
                # Папка с таким названием была
                # Выуживаем объект
                # проверяем наличие файла в списке
                # добавляем в общий список файл
                for td in saveTableDir:
                    if td.pathDir == dirSelection:
                       dir1 = td
            
            for name in selected_files:    # Проход по выделенному списку
                if os.path.isdir(name):    # Проверка названия, что это папка              
                
                    #if name in PathsDir
                    if name not in PathsDir:
                        if self.ui.checkBox_FolderNesting.isChecked():
                            scanDir_typeTableDir(saveTableDir, name)
                else:
                    dir1.setPathFile(name)

            self.tvSourceCodeFiles.setData(saveTableDir)
        
        
        # fdialog = QFileDialog(self,                # Родитель
        #                       "Выберите файлы...", # Название открытого QFileDialog
        #                       self.cwd             # Начальный путь
        #                                               )
        # fdialog.setFileMode(QFileDialog.AnyFile)
        # fdialog.setViewMode(QFileDialog.Detail)
        # fdialog.setFileter(QFileDialog.Files|QFileDialog.Dirs);
        # if fdialog.exec_():
        #     fileNames = dialog.selectedFiles()
        #     print("fileNames")
        #     print(fileNames)
            
        
        # ##!!!!!!! В стадии написания и отладки
        # dir_choose = QFileDialog.getExistingDirectory(self,                # Родитель
        #                                               "Выберите файлы...", # Название открытого QFileDialog
        #                                               self.cwd             # Начальный путь
        #                                               ) 

        # if dir_choose == "":
        #     print("\ nОтменить выбор")
        #     return

        # print("\ nВы выбрали папку:")
        # print(dir_choose)
        
        
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
            
        
        
        
        