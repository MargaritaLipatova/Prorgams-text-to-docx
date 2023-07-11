# -*- coding: utf-8 -*-
"""
__summury__
Created on Sun June 11 2023
@author: Vasilyeva
"""

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *

from common import *
from dialog_ChangeExtensions import dialogChangeExtensions

class TableFilterEx(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super(TableFilterEx, self).__init__()
        self._listEx = set()

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
                # if not (self.sourceModel().data(index, role = Qt.DisplayRole) in filter): # Если какой-либо фильтр присутствует в строке
                #     return True
                #     # return self.sourceModel().data(index).toString().contains(filter)
        except Exception as e:
            print("EROOR = ", e)

        return False

    def setFilterEx(self, sEx):
        self._listEx.add(sEx)

    def removeFilterEx(self, sEx):
        self._listEx.remove(sEx)

    def removeAllFilterEx(self):
        self._listEx.clear()



