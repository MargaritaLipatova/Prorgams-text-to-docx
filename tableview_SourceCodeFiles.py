# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 14:39:51 2023

@author: Vasilyeva
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTableView

#===============================================================================

class cfgTableSourceCodeFiles(object):
    """
        Основные конфигурации для таблицы "Файлы исходных кодов".
    """
    def __init__(self):
        self._countColumn = 3
        self._idColumnCheck = 0
        self._idColumnName = 1
        self._idColumnEx = 2
        self._HHeaderLabels = ["", "Название", "Расширение"]
        self._widthColumnCheck = 10
        self._widthColumnName = 450
        self._widthColumnEx = 100
        
    def countColumn(self):
        return self._countColumn
    
    def idColumnCheck(self):
        return self._idColumnCheck

    def idColumnName(self):
        return self._idColumnName

    def idColumnEx(self):
        return self._idColumnEx
    
    def widthColumnCheck(self):
        return self._widthColumnCheck

    def widthColumnName(self):
        return self._widthColumnName

    def widthColumnEx(self):
        return self._widthColumnEx

    def HHeaderLabels(self):
        return self._HHeaderLabels
    
#===============================================================================

class TableSourceCodeFiles(QTableView):
    """
        Таблица "Файлы исходных кодов".
        Отображено размещение файла, название файла, тип, расширение
    """
    def __init__(self, parent=None):
        super(TableSourceCodeFiles, self).__init__(parent)
        #super(TableSourceCodeFiles, self).__init__()
        #self.setParent(parent)
        self.cfgTable = cfgTableSourceCodeFiles()
        self.tv_model = QStandardItemModel(self) # Модель представления данных в таблице
        self.tv_model.setColumnCount(self.cfgTable.countColumn())          # В моделе устанавливаем 3 колонки
        self.tv_model.setHorizontalHeaderLabels(self.cfgTable.HHeaderLabels()) # Названия 4 колонок (Расширение или Тип)
        self.setModel(self.tv_model)             #Установка модели представления в таблицу
        self.setColumnWidth(self.cfgTable.idColumnCheck(), self.cfgTable.widthColumnCheck())
        self.setColumnWidth(self.cfgTable.idColumnName(),  self.cfgTable.widthColumnName())
        self.setColumnWidth(self.cfgTable.idColumnEx(),    self.cfgTable.widthColumnEx())
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def setRow(self, row, data):
        
        # # Добавление строк в таблицу
        # if self.cfgTable.rowColumn() == 0:
        #     # Таблица была не заполнена, анализ строк не производится            
        #     data.
        # else:
        #     # Таблица была заполнена, анализ названий папок
            
            
            
            
        lst #lst:QList<QStandardItem> = []         
        for i in range(0, self.cfgTable.countColumn()):
            item = QStandardItem(row, i);
            item.setText();
            lst.append(item);

        self.tv_model.appendRow(lst);
        #self.setModel(model);
# =============================================================================
#         for(int row = 0;row<5;row++)
#         {
#             QList<QStandardItem*> lst;
#             for(int column = 0;column<1;column++)
#             {
#                 QStandardItem* item = new QStandardItem(row,column);
#                 item->setText("Бла бла бла");
#                 lst<<item;
#             }
#             model->appendRow(lst);
#         }
#         this->setModel(model);
# =============================================================================
        
        return
    
    
    
        





