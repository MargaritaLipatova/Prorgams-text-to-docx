# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 14:39:51 2023

@author: Vasilyeva
"""
from PyQt5.QtCore import (QAbstractTableModel, QModelIndex, QPoint, QSize, Qt,
                          QVariant)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QHeaderView, QMenu,
                             QPushButton, QTableView)

import loggers
from common import os
from dialog_ChangeExtensions import dialogChangeExtensions
from table_filter import TableFilterEx


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
class TableModel(QAbstractTableModel):
    """ Модель-представления таблицы 'Файлы исходных кодов'
    """
    def __init__(self, cfgTable: cfgTableSourceCodeFiles, parent=None):
        super(TableModel, self).__init__(parent)
        try:
            self.loggers = loggers.get_logger(TableModel.__name__)
            self.loggers.info('Start')
            self.cfgTable = cfgTable     # конфигурация таблицы
            self._intermediateTable = [] # массив данных для модели-представления

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    @property
    def intermediateTable(self):
        return self._intermediateTable

    @intermediateTable.setter
    def intermediateTable(self, data):
        self.loggers.info('Start')
        self._intermediateTable = data
        self.loggers.info(f'Count row table={len(data)}')

    def data(self, index, role):
        """ Отображение данных в таблице.
        """
        try:
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

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._intermediateTable)

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

    def insertRowFiles(self, data: []):
        """ Добавление списка в модель
        Args:
            data ([]): список данных для отображения в таблице
        """
        self.loggers.debug('Start')
        self.beginResetModel()
        self.intermediateTable = data
        self.endResetModel()
        # self.layoutChanged.emit()
        self.loggers.debug('Stop')

    def removeRowExs(self, nameEx: str):
        """ Удаление строк по фильтру

        Args:
            nameEx (str) фильтр
        """
        self.loggers.debug('Start')
        for x in reversed(range(len(self.intermediateTable))):
            if self._intermediateTable[x][2] == nameEx:
                self.beginRemoveRows(QModelIndex(), x, x)
                self._intermediateTable.remove(self._intermediateTable[x])
                self.endRemoveRows()
        # self.layoutChanged.emit()
        self.loggers.debug('Stop')

    def removeRowNmb(self, row: int):
        """ Удаление по номеру строки
        Args:
            row (int) номер строки
        """
        self.loggers.debug('Start')
        self.beginRemoveRows(QModelIndex(), row, row)
        self._intermediateTable.remove(self._intermediateTable[row])
        self.endRemoveRows()
        # self.layoutChanged.emit()
        self.loggers.debug('Stop')

    def removeRowPath(self, path: str):
        """ Удаление по названию пути
        Args:
            path (str) путь к файлу
        """
        self.loggers.debug('Start')
        for x in range(len(self.intermediateTable)):
            if self._intermediateTable[x][3] == path:
                self.beginRemoveRows(QModelIndex(), x, x)
                self._intermediateTable.remove(self._intermediateTable[x])
                self.endRemoveRows()
                break
        self.loggers.debug('Stop')
#===============================================================================


#===============================================================================
class TableSourceCodeFiles(QTableView):
    """
        Таблица "Файлы исходных кодов".
        Отображено размещение файла, название файла, тип, расширение
    """
    def __init__(self, parent=None):
        super(TableSourceCodeFiles, self).__init__(parent)
        try:
            self.loggers = loggers.get_logger(TableSourceCodeFiles.__name__)
            self.loggers.info('Start')
            self.cfgTable:cfgTableSourceCodeFiles = cfgTableSourceCodeFiles()

            self.srcModel:TableModel = TableModel(self.cfgTable, self)
            self.tableFilterEx = TableFilterEx(self)
            self.tableFilterEx.setSourceModel(self.srcModel)
            self.tableFilterEx.setDynamicSortFilter(True)
            self.tableFilterEx.setFilterKeyColumn(self.cfgTable.idColumnEx())
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
            self.filter_pBtn:QPushButton = QPushButton(self.horizontalHeader())
            self.icon_filter_noAction:QIcon = QIcon(QPixmap(":/icon/icon/filter_no_action.png"))
            self.icon_filter_Action:QIcon   = QIcon(QPixmap(":/icon/icon/filter_action.png"))

            self.filter_pBtn.setIcon(self.icon_filter_noAction)
            self.filter_pBtn.setIconSize(QSize(15, 21))
            self.filter_pBtn.show()
            self.filter_pBtn.setStyleSheet("QPushButton{background-color: #c1e1de;\
                                                        color: black;\
                                                        border: 1px solid #6c6c6c;}")
            self.filter_pBtn.clicked.connect(self.btnClicked_filterEx)

            # окно фильтра
            self.dlgFilterEx:dialogChangeExtensions = dialogChangeExtensions(self)

            self.horizontalHeader().sectionResized.connect(self.filter_pBtn_HHeaderSectionResized)
            # self.horizontalHeader().horizontalScrollBar().connect(self.filter_pBtn_HHeaderScrollBar)

            # Контекстное меню
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.ctxMenu)
            self.createContextMenu()

            self.loggers.info('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def filter_pBtn_HHeaderSectionResized(self, logicalIndex, oldSize, newSize):
        """ Обработка сигнала: sectionResized, отвечающего за изменение размера
            заголовка таблицы.
            При возникновение сигнала изменяется положение кнопки 'Фильтр'.
        """
        try:
            self.loggers.info('Start')
            if (logicalIndex + 1) == self.cfgTable.idColumnEx():
                self.filter_pBtn.move(newSize +
                                    self.horizontalHeader().sectionSize(logicalIndex + 1) - # widthColumnEx
                                    self.filter_pBtn.width(), 0)                            # widthBtn # position(x, y)

            self.loggers.info('End')
        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def changeIconFilter(self):
        """ Изменение цвета кнопки 'Фильтр'
        """
        try:
            self.loggers.info('Start')
            self.filter_pBtn.setIcon(self.icon_filter_Action if self.dlgFilterEx.is_filter else self.icon_filter_noAction)
            self.loggers.debug('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')


    def btnClicked_filterEx(self):
        """ Кнопка 'Фильтр' открывает окно с выбором фильтров
        """
        try:
            self.loggers.info('Start')
            pointBtn = self.filter_pBtn.mapToGlobal(QPoint(0,0))
            self.dlgFilterEx.move(pointBtn.x() +
                                self.filter_pBtn.geometry().width() -
                                self.dlgFilterEx.geometry().width(),
                                pointBtn.y() + self.filter_pBtn.height())

            self.dlgFilterEx.exec()
            self.changeIconFilter()

            self.tableFilterEx.removeAllFilterEx()
            for ftr in self.dlgFilterEx.getFilters():
                self.tableFilterEx.setFilterEx(ftr)
            self.loggers.info('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')


    def getAllListTable(self)->set:
        """Возвращает весь список (path)
        Return:
            pathsList (list): список путей к файлам
        """
        try:
            self.loggers.info('Start')
            return set(k[3] for k in self.srcModel.intermediateTable)
        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def getDocxListTable(self)->list:
        """Возвращает список путей к файлам для создания документа
        Return:
         pathsList (list): список путей к файлам
        """
        try:
            self.loggers.info('Start')
            listDocx = []
            for fileRow in self.srcModel.intermediateTable:

                if fileRow[0] is not True:
                    listDocx.append(fileRow[3])

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')
        self.loggers.info('End')

        return listDocx


    def __getIntermediateModel(self, data: set)->[]:
        """ Производится подготовка массива для модели-представления.
            Один элемент(строка модели) представляет список из 4 параметров:
              [0] - фильтр: True  - строка скрыта(галочка -)
                            False - строка видна (галочка +)
              [1] - имя файла
              [2] - имя расширения
              [3] - путь к файлу
        Args:
            data (set): список путей файлов
        Returns:
            []: Массив для модели-представления
        """
        try:
            self.loggers.info('Start')
            self.listEx = []
            intermediateTable = []
            for path in data:
                basename  = os.path.splitext(path)
                file_name = os.path.basename(basename[0])
                ex = basename[-1]
                intermediateTable.append(   [False,       # statehiddenfilters
                                            file_name,    # basename.split('.')[0], # name file
                                            ex,           # ex
                                            path          # path
                                            ])

                if not ex in self.listEx:
                    self.listEx.append(ex)
                    self.tableFilterEx.setFilterEx(ex)

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')
        self.loggers.info('End')

        return intermediateTable

    def setInfoModel(self, data: set)->None:
        """ Установка вида модели для отображения в таблице
        Args:
            data (set): список файлов
        """
        try:
            self.loggers.info('Start')
            intermediateTable = self.__getIntermediateModel(data)
            # -----------------------------------
            self.setActionEx()
            self.setTableFilterEx()
            # -----------------------------------
            self.srcModel.insertRowFiles(intermediateTable)
            self.loggers.info('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def setTableFilterEx(self):
        """ Добавление расширений в фильтр
        """
        try:
            self.loggers.info('Start')
            self.dlgFilterEx.setFilters(self.listEx)
            # self.dlgFilterEx.removeFilter(self.listEx[0])
            self.loggers.info('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def setActionEx(self):
        """ Очищение и добавление расширений в меню "Удалить файлы по расширению"
        """
        try:
            self.loggers.info('Start')
            self.menuDeleteFilesEx.clear()
            for ex in self.listEx:
                actEx = QAction(ex, self)
                actEx.triggered.connect(self.deleteFilesEx)
                self.menuDeleteFilesEx.addAction(actEx)
            self.loggers.info('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def ctxMenu(self, pos):
        """ Обработка сигнала вызова контекстного меню по нажатию правой кнопки мыши
        Args:
            pos (_type_): позиция курсора мыши
        """
        try:
            self.loggers.info('Start')
            self.actionDeleteFile.setEnabled( False if len(self.srcModel.intermediateTable) == 0 else True)
            self.menuDeleteFilesEx.setEnabled(False if len(self.srcModel.intermediateTable) == 0 else True)
            self.qMenuTable.exec(self.mapToGlobal(pos))
            self.loggers.info('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def deleteFile(self):
        """ Удаление одного файла по кнопке контекстного меню "Удалить"
        """
        try:
            self.loggers.info('Start')
            name = None
            nameEx = None
            namePath = None
            for index in self.selectionModel().selectedIndexes():
                if index.column()== self.cfgTable.idColumnName():
                    name = index.data(role=Qt.DisplayRole)
                    namePath = index.data(role=Qt.ToolTipRole)
                elif index.column()== self.cfgTable.idColumnEx():
                    nameEx = index.data(role=Qt.DisplayRole)

            self.loggers.info( f"selection: text = {name} , ex = {nameEx}, path = {namePath}")

            if namePath or name or nameEx:
                self.srcModel.removeRowPath(namePath)

                # проверка не был ли этот файл единственным с таким расширением
                if not any(item for item in self.srcModel.intermediateTable if item[2] == nameEx):
                    self.tableFilterEx.removeFilterEx(nameEx)
                    self.listEx.remove(nameEx)
                    self.dlgFilterEx.removeFilter(nameEx)

                    for pObj in self.menuDeleteFilesEx.actions():
                        if pObj.text() == nameEx:
                            self.menuDeleteFilesEx.removeAction(pObj)
                            break
            else:
                self.loggers.warning("Don`t selection row")
                self.loggers.warning(f"selection: text = {name} , ex = {nameEx}, path = {namePath}")

            self.loggers.debug('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def deleteFilesEx(self):
        """ Удаление файлов по кнопке контекстного меню "Удалить файлы по расширению"
        """
        try:
            self.loggers.info('Start')
            pObj = self.sender()
            nameEx =  pObj.text()
            self.loggers.debug("deleteFilesEx", nameEx)

            self.srcModel.removeRowExs(nameEx)
            self.tableFilterEx.removeFilterEx(nameEx)
            self.listEx.remove(nameEx)
            self.dlgFilterEx.removeFilter(nameEx)
            self.menuDeleteFilesEx.removeAction(pObj)

            self.loggers.debug('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')


    def createContextMenu(self):
        """ Создание контекстного меню таблицы
        """
        try:
            self.loggers.info('Start')
            self.actionDeleteFile = QAction("Удалить", self)
            self.actionDeleteFile.triggered.connect(self.deleteFile)
            self.actionDeleteFile.setEnabled(False)

            self.menuDeleteFilesEx = QMenu("Удалить файлы по расширению", self)
            self.menuDeleteFilesEx.setEnabled(False)

            self.qMenuTable = QMenu(self)
            self.qMenuTable.addAction(self.actionDeleteFile)
            self.qMenuTable.addMenu(self.menuDeleteFilesEx)
            self.loggers.debug('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')
#===============================================================================


