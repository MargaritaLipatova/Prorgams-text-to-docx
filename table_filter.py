# -*- coding: utf-8 -*-
"""
     Файл содержит реализацию proxy модели, которая является
    посредником между таблицей и моделью представления.
     ProxyModel осуществляет фильтрацию строк и записывает в модель представления
    состояние строки по фильтру([0]) .

    Created on Sun June 11 2023
@author: Vasilyeva
"""

from PyQt5.QtCore import QModelIndex, QSortFilterProxyModel, Qt

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
            count = len(self.sourceModel().intermediateTable)

            # Проверка!!!
            # Модель не сразу заполняется.
            # В массиве sourceModel().intermediateTable может не быть
            # ещё строки sourceRow. И произойдет выход за пределы массива.
            if count <= 0 or count <= sourceRow:
                return False

            if textEx in self._listEx:
                # Строка видна
                self.sourceModel().intermediateTable[sourceRow][0] = False
                return True
            else:
                # Строка скрыта
                self.sourceModel().intermediateTable[sourceRow][0] = True
                return False
        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

        return False

    def setFilterEx(self, sEx: str):
        """ Устанавка одного фильтра

        Args:
            sEx (str): имя фильтра
        """
        self.loggers.info('Start')
        self._listEx.add(sEx)
        self.invalidateFilter()

    def setFilters(self, set_list: set):
        """ Устанавка set
        Args:
            sEx (set): список расширений
        """
        self.loggers.info('Start')
        self._listEx = set_list
        self.invalidateFilter()

    def removeFilterEx(self, sEx: str):
        """ Удаление одного фильтра

        Args:
            sEx (str): имя фильтра
        """
        self.loggers.info('Start')
        self._listEx.remove(sEx)
        self.invalidateFilter()

    def removeAllFilterEx(self):
        """Очистка спсика фильтра
        """
        self.loggers.info('Start')
        self._listEx.clear()
        self.invalidateFilter()



