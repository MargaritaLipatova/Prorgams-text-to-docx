# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:24:09 2022

@author: Vasilyeva
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from ui_files.ui_ishod_w import Ui_DialogIshodDocx  # импорт нашего сгенерированного файла
from dialog_ChangeExtensions import dialogChangeExtensions  
import os

class dialogIshodDocx(QtWidgets.QDialog):
    """ Главное диалоговое окно 'Исход-В'
    """
    def __init__(self, parent=None):
        super(dialogIshodDocx, self).__init__()
        self.ui = Ui_DialogIshodDocx() # Инициализация ui-интерфейсов
        self.ui.setupUi(self)          # Установка ui-интерфейсов
        self.cwd = os.getcwd()         # Получить текущее местоположение файла программы

        

        # Виджет с информацией о расширениях
        self.ui.wStatusExtensions.setVisible(False) # скрыть информацию
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
        ##!!!!!!! В стадии написания и отладки
        dir_choose = QFileDialog.getExistingDirectory(self,                # Родитель
                                                      "Выберите файлы...", # Название открытого QFileDialog
                                                      self.cwd             # Начальный путь
                                                      ) 

        if dir_choose == "":
            print("\ nОтменить выбор")
            return

        print("\ nВы выбрали папку:")
        print(dir_choose)
        
        
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
                            "All Files (*);;Text Files (*.txt)")  

        if fileName_choose == "":
            print("\ nОтменить выбор")
            return

        print("\ nФайл, который вы выбрали для сохранения:")
        print(fileName_choose)
        print("Тип фильтра файлов:",filetype)
            
        
        
        
        