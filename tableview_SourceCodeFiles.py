# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 14:39:51 2023

@author: Vasilyeva
"""



from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *

from common import *
from dialog_ChangeExtensions import dialogChangeExtensions
from table_filter import *

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

    def HHeaderSheetStyle(self):
        return "::section \
                { \
                    background-color: #c1e1de;\
                    color: black;\
                    border: 1px solid #6c6c6c;\
                }"
#===============================================================================



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

        self.cfgTable = cfgTableSourceCodeFiles()
        self.model    = TableModel([],self.cfgTable)

        self.tableFilterEx = TableFilterEx()
        # self.tableFilterEx.setDynamicSortFilter(True)
        self.tableFilterEx.setFilterKeyColumn(self.cfgTable.idColumnEx())
        self.tableFilterEx.setSourceModel(self.model)
        self.setModel(self.tableFilterEx)

        self.setColumnWidth(self.cfgTable.idColumnName(),  self.cfgTable.widthColumnName())
        self.setColumnWidth(self.cfgTable.idColumnEx(),    self.cfgTable.widthColumnEx())
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.horizontalHeader().setStretchLastSection(True)                    # Растягивание последнего столбца, если изменился размер таблицы
        self.horizontalHeader().setSectionResizeMode(self.cfgTable.idColumnName(), QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(self.cfgTable.idColumnEx(), QHeaderView.Interactive)
        self.horizontalHeader().setStyleSheet(self.cfgTable.HHeaderSheetStyle())
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.verticalHeader().setVisible(False)

        self.listEx = []        # список расширений для колонки "Тип"

        # Фильтр на колонку "Тип"
        self.filter_pBtn          = QPushButton(self.horizontalHeader())
        self.icon_filter_noAction = QtGui.QIcon(QtGui.QPixmap(":/icon/icon/filter_no_action.png"))
        self.icon_filter_Action   = QtGui.QIcon(QtGui.QPixmap(":/icon/icon/filter_action.png"))

        self.filter_pBtn.setIcon(self.icon_filter_noAction)
        self.filter_pBtn.setIconSize(QSize(15, 21))
        self.filter_pBtn.show()
        self.filter_pBtn.setStyleSheet("QPushButton{ \
                    background-color: #c1e1de;\
                    color: black;\
                    border: 1px solid #6c6c6c;\
                }")
        self.filter_pBtn.clicked.connect(self.btnClicked_filterEx)

        # окно фильтра
        self.dlgFilterEx = dialogChangeExtensions(self)

        self.horizontalHeader().sectionResized.connect(self.filter_pBtn_HHeaderSectionResized)
        # self.horizontalHeader().horizontalScrollBar().connect(self.filter_pBtn_HHeaderScrollBar)

        # Контекстное меню
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ctxMenu)
        self.createContextMenu()

    def filter_pBtn_HHeaderSectionResized(self, logicalIndex, oldSize, newSize):
        if (logicalIndex + 1) == self.cfgTable.idColumnEx():
            self.filter_pBtn.move(newSize +                                               # newSize
                                  self.horizontalHeader().sectionSize(logicalIndex + 1) - # widthColumnEx
                                  self.filter_pBtn.width(), 0)                            # widthBtn # position(x, y)


    def changeIconFilter(self):
        self.filter_pBtn.setIcon(self.icon_filter_Action if self.dlgFilterEx.is_filter else self.icon_filter_noAction)
        # if self.dlgFilterEx.is_filter:
        #     self.filter_pBtn.setIcon(self.icon_filter_noAction)
        #     self.dlgFilterEx.is_filter = False
        # else:
        #     self.filter_pBtn.setIcon(self.icon_filter_Action)
        #     self.dlgFilterEx.is_filter = True

    def btnClicked_filterEx(self):
        pointBtn = self.filter_pBtn.mapToGlobal(QPoint(0,0))
        self.dlgFilterEx.move(pointBtn.x() +
                              self.filter_pBtn.geometry().width() -
                              self.dlgFilterEx.geometry().width(),
                              pointBtn.y() + self.filter_pBtn.height())

        if self.dlgFilterEx.exec() == QDialog.Accepted:
            print("OK exit dlgFilterEx")
        else:
            print("Cancel exit dlgFilterEx")
        self.changeIconFilter()

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
            basename  = os.path.splitext(path)
            file_name = os.path.basename(basename[0])
            ex = basename[-1] #str(os.path.basename(name).suffix) #str(basename.split(basename.split('.')[0])[-1])
            intermediateTable.append(   [False,       # statehiddenfilters
                                        file_name,    # basename.split('.')[0], # name file
                                        ex,           # ex
                                        path          # path
                                        ])

            if not ex in self.listEx:
                self.listEx.append(ex)
                self.tableFilterEx.setFilterEx(ex)

        return intermediateTable

    def setInfoModel(self, data: set)->None:
        # -----------------------------------
        # Промежуточный вид модели для отображения в таблице
        # -----------------------------------
        intermediateTable = self.__getIntermediateModel(data)
        # -----------------------------------
        self.setActionEx()
        self.setTableFilterEx()
        # -----------------------------------
        self.model.intermediateTable = intermediateTable
        self.model.dataSrc = data
        self.model.layoutChanged.emit()

    def setTableFilterEx(self):
        self.dlgFilterEx.setFilters(self.listEx)
        # self.dlgFilterEx.removeFilter(self.listEx[0])

    def setActionEx(self):
        """
            Очищение и добавление расширений в меню "Удалить файлы по расширению"
        """
        self.menuDeleteFilesEx.clear()
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
        self.qMenuTable.exec(self.mapToGlobal(pos))

    def deleteFile(self):
        try:
            selrow = self.selectionModel().currentIndex().row()
            print("selection", selrow,
                ", text ", self.model.intermediateTable[selrow][1],
                ", ex ", self.model.intermediateTable[selrow][2])

            self.blockSignals(True)
            self.model.dataSrc.remove(self.model.intermediateTable[selrow][3])
            self.model.intermediateTable.remove(self.model.intermediateTable[selrow])
            self.blockSignals(False)

            # Обновление строк в таблице
            self.model.updateCountRow()
            # self.model.layoutChanged.emit()

            # !!!!!!!!!
            # проверка не был ли этот файл единственным с таким расширением
            # !!!!!!!!!
        except Exception as e:
            print("EROOR = ", e)

    def deleteFilesEx(self):
        try:
            pObj = self.sender()
            nameEx =  pObj.text()
            print("deleteFilesEx", nameEx)

            # Удаление из промежуточной таблицы, то что отображается в таблице
            for x in reversed(range(len(self.model.intermediateTable))):
                if self.model.intermediateTable[x][2] == nameEx:
                    self.model.intermediateTable.remove(self.model.intermediateTable[x])

            # Удаление из модели
            for x in reversed(range(len(self.model.dataSrc))):
                if os.path.splitext(list(self.model.dataSrc)[x])[-1] == nameEx:
                    self.model.dataSrc.remove(list(self.model.dataSrc)[x])

            # Обновление строк в таблице
            self.model.updateCountRow()
            self.tableFilterEx.removeFilterEx(nameEx)
            self.listEx.remove(nameEx)

            self.menuDeleteFilesEx.removeAction(pObj)

            if self.menuDeleteFilesEx.isEmpty():
                self.menuDeleteFilesEx.setDisabled(True)

            # self.model.layoutChanged.emit()

        except Exception as e:
            print("EROOR = ", e)


    def createContextMenu(self):
        self.actionDeleteFile = QAction("Удалить", self)
        # self.actionDeleteFile.setStatusTip("Create a new file")
        self.actionDeleteFile.triggered.connect(self.deleteFile)
        self.actionDeleteFile.setEnabled(False)

        self.menuDeleteFilesEx = QMenu("Удалить файлы по расширению", self)
        # self.menuDeleteFilesEx.triggered.connect(self.deleteFilesEx)
        self.menuDeleteFilesEx.setEnabled(False)

        self.qMenuTable = QMenu(self)
        self.qMenuTable.addAction(self.actionDeleteFile)
        self.qMenuTable.addMenu(self.menuDeleteFilesEx)
