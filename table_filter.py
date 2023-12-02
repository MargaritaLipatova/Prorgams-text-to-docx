# -*- coding: utf-8 -*-
"""
__summury__
Created on Sun June 11 2023
@author: Vasilyeva
"""

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex
import loggers

class TableFilterEx(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(TableFilterEx, self).__init__(parent)

        try:
            self.loggers = loggers.get_logger(TableFilterEx.__name__)
            self.loggers.info('Start')
            self._listEx = set()

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def filterAcceptsRow(self, sourceRow: int, sourceParent: QModelIndex):
        try:
            index: QModelIndex = self.sourceModel().index(sourceRow, self.filterKeyColumn(), sourceParent)
            textEx = self.sourceModel().data(index, role = Qt.DisplayRole)

            if textEx in self._listEx:
                # Строка видна
                self.sourceModel().intermediateTable[sourceRow][0] = False
                return True
            else:
                # Строка скрыта
                self.sourceModel().intermediateTable[sourceRow][0] = True
                return False
                # if not (self.sourceModel().data(index, role = Qt.DisplayRole) in filter): # Если какой-либо фильтр присутствует в строке
                #     return True
                #     # return self.sourceModel().data(index).toString().contains(filter)
        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

        return False

    def setFilterEx(self, sEx):
        self.loggers.info('Start')
        self._listEx.add(sEx)

    def removeFilterEx(self, sEx):
        self.loggers.info('Start')
        self._listEx.remove(sEx)

    def removeAllFilterEx(self):
        self.loggers.info('Start')
        self._listEx.clear()



