# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 14:39:51 2023

@author: Vasilyeva
"""
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import QTableView


from PyQt5 import QtCore, QtGui, QtWidgets, uic#, QVariant, QString
from PyQt5.QtCore import Qt, QVariant #№, QString
from common import *
#===============================================================================

class cfgTableSourceCodeFiles(object):
    """
        Основные конфигурации для таблицы "Файлы исходных кодов".
    """
    def __init__(self):
        self._countColumn = 2
#        self._idColumnCheck = 0
        self._idColumnName = 0
        self._idColumnEx = 1
        self._HHeaderLabels = ["Название", "Тип"]
        # self._widthColumnCheck = 10
        self._widthColumnName = 450
        self._widthColumnEx = 100
        
    
    def countColumn(self):
        return self._countColumn
    
    # def idColumnCheck(self):
    #     return self._idColumnCheck
    
    def idColumnName(self):
        return self._idColumnName
    
    def idColumnEx(self):
        return self._idColumnEx
    
    # def widthColumnCheck(self):
    #     return self._widthColumnCheck

    def widthColumnName(self):
        return self._widthColumnName

    def widthColumnEx(self):
        return self._widthColumnEx

    def HHeaderLabels(self):
        return self._HHeaderLabels

    def HHeaderSheetStyle(self):
        return "::section \
                { \
                    background-color: #c1e1de;\
                    color: black;\
                    border: 1px solid #6c6c6c;\
                }"
#===============================================================================


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, cfgTable):
        super(TableModel, self).__init__()
        self._dataSrc = data or []
        self.cfgTable = cfgTable
        self.countRow = 0
        self._intermediateTable = []
        
    @property
    def intermediateTable(self):
        return self._intermediateTable
    
    @intermediateTable.setter
    def intermediateTable(self, data):
        self._intermediateTable = data
        self.countRow = len(data)
        
    @property
    def dataSrc(self):
        return self._dataSrc
    
    @dataSrc.setter
    def dataSrc(self, data):
        self._dataSrc = data  
    
    # def setData(self, index, value, role=QtCore.Qt.EditRole):
    #     # if role == QtCore.Qt.EditRole:
    #     #     row = index.row()
    #     #     column = index.column()
    #     #     self.materials[row][column] = value
    #     #     self.dataChanged.emit(index, index, (role,))
    #     #     return True
    #     if role == QtCore.Qt.CheckStateRole:
    #         #self.check_states[QtCore.QPersistentModelIndex(index)] = value
    #         self.dataChanged.emit(index, index, (role,))
    #         return True
    #     return False
    
    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
            if index.column() == self.cfgTable.idColumnEx():
                return Qt.AlignCenter
            
            
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list

            if index.column() == self.cfgTable.idColumnEx():
                return self.intermediateTable[index.row()][2]
            
            if index.column() == self.cfgTable.idColumnName():
                return self.intermediateTable[index.row()][1]

        # if role == QtCore.Qt.CheckStateRole:
        #     if index.column() == self.cfgTable.idColumnCheck():
        #         value = self.intermediateTable[index.row()][0] #self.check_states.get(QtCore.QPersistentModelIndex(index))
        #         if value is not None:
        #             return value
            

    def rowCount(self, index):
        # The length of the outer list.
        # countRow = 0
        # for dt in self.dataSrc: 
        #     countRow += 1
        #     countRow += len(dt.pathFiles)
        return self.countRow

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self.cfgTable.countColumn()
    
    def headerData(self, section:int, orientation:Qt.Orientation, role:int):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Название"
                elif section == 1:
                    return "Тип"
        return QVariant()
    
#     def flags(self, index):
#         if index.column() == self.cfgTable.idColumnCheck():
#             return (QtCore.Qt.ItemIsEditable  | QtCore.Qt.ItemIsEnabled| 
#                     QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsUserCheckable)

# =============================================================================
# 
# class CustomDelegate(QtWidgets.QStyledItemDelegate):
#     def initStyleOption(self, option, index):
#         if index.column() == 0:#self.cfgTable.idColumnCheck():
#             value = index.data(QtCore.Qt.CheckStateRole)
#             if value is None:
#                 model = index.model()
#                 model.setData(index, QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
#             super().initStyleOption(option, index)
#             option.direction = QtCore.Qt.RightToLeft
#             option.displayAlignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter

# =============================================================================

class TableSourceCodeFiles(QTableView):
    """
        Таблица "Файлы исходных кодов".
        Отображено размещение файла, название файла, тип, расширение
    """
    def __init__(self, parent=None):
        super(TableSourceCodeFiles, self).__init__(parent)
        self.cfgTable = cfgTableSourceCodeFiles()
        self.model = TableModel([],self.cfgTable)
        # self.model.setHorizontalHeaderLabels(self.cfgTable.HHeaderLabels())  # Названия 4 колонок (Расширение или Тип)
        # self.model.setColumnCount(self.cfgTable.countColumn())
        self.setModel(self.model)
        # delegate = CustomDelegate(self)
        # self.setItemDelegateForColumn(self.cfgTable.idColumnCheck(), delegate)

        #self.tv_model = QStandardItemModel(self)                                # Модель представления данных в таблице
        #self.model.setColumnCount(self.cfgTable.countColumn())               # В моделе устанавливаем 3 колонки
        #self.model.setHorizontalHeaderLabels(self.cfgTable.HHeaderLabels())  # Названия 4 колонок (Расширение или Тип)
        #self.setModel(self.tv_model)                                            # Установка модели представления в таблицу
        # self.setColumnWidth(self.cfgTable.idColumnCheck(), self.cfgTable.widthColumnCheck())
        self.setColumnWidth(self.cfgTable.idColumnName(),  self.cfgTable.widthColumnName())
        self.setColumnWidth(self.cfgTable.idColumnEx(),    self.cfgTable.widthColumnEx())
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)                    # Растягивание последнего столбца, если изменился размер таблицы
        self.horizontalHeader().setStyleSheet(self.cfgTable.HHeaderSheetStyle())
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)


       
        self._pathsList: list = []                                             # Список путей к папкам и файлам в таблице
        self._pathsDir:  list = []                                             # Список путей к папкам и файлам в таблице
        self._tableDir:  list = []
        self._countRow = 0

    def setPathsList(self, pathsList:list):
        """Добавляет список путей к папкам и файлам
        Args:
            pathsList (list): список путей к папкам и файлам
        """
        self._pathsList.append(pathsList)
    
    def getPathsList(self, pathsList:list)->list:
        """Возвращает список путей к папкам и файлам
        Return:
            pathsList (list): список путей к папкам и файлам
        """
        return self._pathsList
    
    def getPathsDir(self)->list:
      """Возвращает список папок(path)
      Return:
          pathsList (list): список путей к папкам и файлам
      """
      listDir = []
      for idir in self._tableDir:
          listDir.append(idir.pathDir)
      return listDir
  
    def getTableDir(self)->list:
      """Возвращает список папок(path)
      Return:
          pathsList (list): список путей к папкам и файлам
      """
      return self._tableDir
  

    def setData(self, data: list)->None:
        # -----------------------------------
        # Промежуточный вид модели для отображения в таблице
        # -----------------------------------
        intermediateTable = []
        for dirdata in data:
            # папка
            intermediateTable.append([dirdata.checkboxDir, dirdata.pathDir, "Folder"])
            # файлы
            for pathFile in dirdata.pathFiles:
                for name, checkState in pathFile.items():
                    intermediateTable.append(    [checkState, 
                                                  name.split('.')[0].split('/')[-1], 
                                                  name.split('.')[1]
                                                 ])
        # -----------------------------------
        self.model.intermediateTable = intermediateTable
        self.model.dataSrc = data
        self.model.layoutChanged.emit()
         



            
# =============================================================================
#     def __init__(self, parent=None):
#         super(TableSourceCodeFiles, self).__init__(parent)
#         #super(TableSourceCodeFiles, self).__init__()
#         #self.setParent(parent)
#         self.cfgTable = cfgTableSourceCodeFiles()
#         self.tv_model = QStandardItemModel(self)                                # Модель представления данных в таблице
#         self.tv_model.setColumnCount(self.cfgTable.countColumn())               # В моделе устанавливаем 3 колонки
#         self.tv_model.setHorizontalHeaderLabels(self.cfgTable.HHeaderLabels())  # Названия 4 колонок (Расширение или Тип)
#         self.setModel(self.tv_model)                                            # Установка модели представления в таблицу
#         self.setColumnWidth(self.cfgTable.idColumnCheck(), self.cfgTable.widthColumnCheck())
#         self.setColumnWidth(self.cfgTable.idColumnName(),  self.cfgTable.widthColumnName())
#         self.setColumnWidth(self.cfgTable.idColumnEx(),    self.cfgTable.widthColumnEx())
#         self.setEditTriggers(QAbstractItemView.NoEditTriggers)
#         self.horizontalHeader().setStretchLastSection(True)                    # Растягивание последнего столбца, если изменился размер таблицы
#         
#         self._pathsList: list = []                                             # Список путей к папкам и файлам в таблице
#         self._pathsDir:  list = []                                             # Список путей к папкам и файлам в таблице
#         self._tableDir:  list = []
#         self._countRow = 0
#     def setPathsList(self, pathsList:list):
#         """Добавляет список путей к папкам и файлам
#         Args:
#             pathsList (list): список путей к папкам и файлам
#         """
#         self._pathsList.append(pathsList)
#     
#     def getPathsList(self, pathsList:list)->list:
#         """Возвращает список путей к папкам и файлам
#         Return:
#             pathsList (list): список путей к папкам и файлам
#         """
#         return self._pathsList
#     
#     def getPathsDir(self)->list:
#       """Возвращает список папок(path)
#       Return:
#           pathsList (list): список путей к папкам и файлам
#       """
#       listDir = []
#       for idir in self._tableDir:
#           listDir.append(idir.pathDir)
#       return listDir
#   
#     def getTableDir(self)->list:
#       """Возвращает список папок(path)
#       Return:
#           pathsList (list): список путей к папкам и файлам
#       """
#       return self._tableDir
#   
#     
#     def setRow(self, name: str, row, col):
#         item_ = self.tv_model.item(row, self.cfgTable.idColumnName());
#         item_.setText(name)
#         
#     def setFolder(self, data: tableDir):
#         print("1")
#         self.setRow(data.pathDir, self._countRow, self.cfgTable.idColumnName())
#         self._countRow += 1
# 
#         for name in data.pathFiles:
#             self.setRow(name.split('/')[-1].split('.')[0], self._countRow, self.cfgTable.idColumnName())
#             self.setRow(name.split('/')[-1].split('.')[-1], self._countRow, self.cfgTable.idColumnEx())
#             self._countRow += 1
#   
#         #lst.append(item);
#         #self.tv_model.appendRow(lst);
#     
#     def setData(self, data: list)->None:
#         # Количество строк для таблицы
#         countRow = 0
#         
#         for dt in data: 
#             countRow += 1
#             countRow += len(dt.pathFiles)
#         
#         # Выделяем сразу строки в таблицу
#         self.tv_model.setRowCount(countRow)
#         
#         # Запись папки 
#         self._countRow = 0
#         for tdir in data:
#             self.setFolder(tdir)
#             
#         
#             
#         
#         # for i in range(0, self.cfgTable.countColumn()):
#         #     item = QStandardItem(row, i);
#         #     item.setText();
#         #     lst.append(item);
# 
#         # self.tv_model.appendRow(lst);
#         #self.setModel(model);
# # =============================================================================
# #         for(int row = 0;row<5;row++)
# #         {
# #             QList<QStandardItem*> lst;
# #             for(int column = 0;column<1;column++)
# #             {
# #                 QStandardItem* item = new QStandardItem(row,column);
# #                 item->setText("Бла бла бла");
# #                 lst<<item;
# #             }
# #             model->appendRow(lst);
# #         }
# #         this->setModel(model);
# # =============================================================================
#         
#         return
#     
#     
#     
#         
# 
# 
# 
# 
# 
# 
# =============================================================================
