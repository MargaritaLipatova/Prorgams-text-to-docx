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


from PyQt5 import QtCore, QtGui, QtWidgets, uic#, QVariant, QString
from PyQt5.QtCore import * #Qt, QVariants#№, QString
from common import *
#===============================================================================

class cfgTableSourceCodeFiles(object):
    """
        Основные конфигурации для таблицы "Файлы исходных кодов".
    """
    def __init__(self):
        self._countColumn = 2
        self._idColumnName = 0
        self._idColumnEx = 1
        self._HHeaderLabels = ["Название", "Тип"]
        self._widthColumnName = 450
        self._widthColumnEx = 100


    def countColumn(self):
        return self._countColumn

    def idColumnName(self):
        return self._idColumnName

    def idColumnEx(self):
        return self._idColumnEx

    def widthColumnName(self):
        return self._widthColumnName

    def widthColumnEx(self):
        return self._widthColumnEx

    def HHeaderLabels(self):
        return self._HHeaderLabels
    
#===============================================================================


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, cfgTable):
        super(TableModel, self).__init__()
        self._dataSrc = data or set()
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

    def updateCountRow(self):
        self.countRow = len(self._intermediateTable)


    @property
    def dataSrc(self):
        return self._dataSrc

    @dataSrc.setter
    def dataSrc(self, data):
        self._dataSrc = data

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

        if role == Qt.ToolTipRole:
            if index.column() == self.cfgTable.idColumnName():
                return self.intermediateTable[index.row()][3]


    def rowCount(self, index):
        # The length of the outer list.
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

#===============================================================================



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
        self.model = TableModel([],self.cfgTable)
        self.setModel(self.model)
        self.setColumnWidth(self.cfgTable.idColumnName(),  self.cfgTable.widthColumnName())
        self.setColumnWidth(self.cfgTable.idColumnEx(),    self.cfgTable.widthColumnEx())
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.horizontalHeader().setStretchLastSection(True)                    # Растягивание последнего столбца, если изменился размер таблицы
        self.horizontalHeader().setSectionResizeMode(self.cfgTable.idColumnName(), QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(self.cfgTable.idColumnEx(), QHeaderView.Interactive)
        self.horizontalHeader().setStyleSheet(self.cfgTable.HHeaderSheetStyle())
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)

        self.listEx = []        # список расширений

        # Контекстное меню
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ctxMenu)
        self.createContextMenu()

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

    def getAllListTable(self)->list:
      """Возвращает весь список (path)
      Return:
          pathsList (list): список путей к файлам
      """
      return self.model.dataSrc

    def getDocxListTable(self)->list:
        """Возвращает список путей к файлам для создания документа
      Return:
         pathsList (list): список путей к файлам
      """
        listDocx = []
        for fileRow in self.model.intermediateTable:

            if fileRow[0] != True:
                listDocx.append(fileRow[3])
        return listDocx


    def __getIntermediateModel(self, data: set):
        self.listEx = []
        intermediateTable = []
        for path in data:
            print(path)
            basename = os.path.splitext(path)
            file_name = os.path.basename(basename[0])
            ex = basename[-1] #str(os.path.basename(name).suffix) #str(basename.split(basename.split('.')[0])[-1])
            intermediateTable.append(   [False,      # statehidden
                                        file_name,    # basename.split('.')[0], # name file
                                        ex,           # ex
                                        path          # path
                                                 ])

            if not ex in self.listEx:
                        self.listEx.append(ex)

        return intermediateTable

    def setInfoModel(self, data: set)->None:
        # -----------------------------------
        # Промежуточный вид модели для отображения в таблице
        # -----------------------------------
        intermediateTable = self.__getIntermediateModel(data)
        # -----------------------------------
        self.setActionEx()
        # -----------------------------------
        self.model.intermediateTable = intermediateTable
        self.model.dataSrc = data
        self.model.layoutChanged.emit()
        # self.model..emit()

    def setActionEx(self):
        """
            Очищение и добавление расширений в меню "Удалить файлы по расширению"
        """
        self.menuDeleteFilesEx.clear()# Удаление всех расширений
        for ex in self.listEx:
            actEx = QAction(ex, self)
            actEx.triggered.connect(self.deleteFilesEx)
            self.menuDeleteFilesEx.addAction(actEx)

    def ctxMenu(self, pos):
        # -----------------------------------
        # Обработка сигнала вызова контекстного меню по нажатию правой кнопки мыши
        # -----------------------------------
        self.actionDeleteFile.setEnabled( False if len(self.model.dataSrc) == 0 else True)
        self.menuDeleteFilesEx.setEnabled(False if len(self.model.dataSrc) == 0 else True)
        # self.actionDeleteFile.setEnabled( False if len(self.model.intermediateTable) == 0 else True)
        # self.menuDeleteFilesEx.setEnabled(False if len(self.model.intermediateTable) == 0 else True)
        self.qMenuTable.exec(self.mapToGlobal(pos))

    def deleteFile(self):
        print("deleteFile")
        selrow = self.selectionModel().currentIndex().row()
        print("selection", selrow)
        print(" text ", self.model.intermediateTable[selrow][1])
        print(" ex ", self.model.intermediateTable[selrow][2])
        self.model.intermediateTable.remove(self.model.intermediateTable[selrow])

# #
# # !!!!!!!!!!! Скрыть элемент строки
# #
        # for sel in selection:
        #     print('row', sel.row())
        #     self.setRowHidden(sel.row(), True)

    def deleteFilesEx(self):
        pObj = self.sender()
        nameEx =  pObj.text()
        print("deleteFilesEx", nameEx)

        # Удаление из промежуточной таблицы
        for x in reversed(range(len(self.model.intermediateTable))):
            if self.model.intermediateTable[x][2] == nameEx:
                print(x)
                self.model.intermediateTable.remove(self.model.intermediateTable[x])

        # for tab in self.model.dataSrc:
        #     print(tab.pathFiles)
        #     for dictTab in tab.pathFiles:
        #         for k in dictTab.keys():
        #             if k.split('/')[-1].split('.')[1] == nameEx:
        #                 print(k)
        #                 del dictTab[k]
                        # del tab.pathFiles[k]

        self.model.updateCountRow()
        self.menuDeleteFilesEx.removeAction(pObj)

        if self.menuDeleteFilesEx.isEmpty():
            self.menuDeleteFilesEx.setDisabled(True)
        self.model.layoutChanged.emit()

    def createContextMenu(self):
        self.actionDeleteFile = QAction("Удалить", self)
        self.actionDeleteFile.setStatusTip("Create a new file")
        self.actionDeleteFile.triggered.connect(self.deleteFile)
        self.actionDeleteFile.setEnabled(False)

        self.menuDeleteFilesEx = QMenu("Удалить файлы по расширению", self)
        self.menuDeleteFilesEx.setEnabled(False)

        self.qMenuTable = QMenu(self)
        self.qMenuTable.addAction(self.actionDeleteFile)
        self.qMenuTable.addMenu(self.menuDeleteFilesEx)
