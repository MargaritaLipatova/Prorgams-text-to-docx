# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 23:49:35 2022

@author: Vasilyeva
"""

# from PyQt5 import QtGui, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QListWidgetItem
from ui_files.ui_dialogChangeExtensions import Ui_dialogChangeExtensions # импорт нашего сгенерированного файла
import loggers

class dialogChangeExtensions(QDialog, Ui_dialogChangeExtensions):
    """ Диалоговое окно 'Изменить расширения...'.
        Отображает расширения всех файлов
        находящихся в таблице "Файлы исходных кодов".
        Перед каждым расширением есть checkBox
        Если галочка установлена, то файл с этим расширением будет
        отображаться в таблице, иначе будет скрыт.
    """
    def __init__(self, parent=None, filterEx=[]):
        super(dialogChangeExtensions, self).__init__(parent)
        try:
            self.loggers = loggers.get_logger(dialogChangeExtensions.__name__)
            self.loggers.info('Start')
            self.ui = Ui_dialogChangeExtensions()        # Инициализация ui-интерфейсов
            self.ui.setupUi(self)                 # Установка ui-интерфейсов
            # self.ui.pBtn_Ok.clicked.connect(self.btnClicked_Ok)            # "Изменить расширения..."
            # self.ui.pBtn_Cancel.clicked.connect(self.btnClicked_Cancel)    # "Добавить файлы из папки..."
            self._is_filter = False
            self.setWindowFlags(Qt.Popup) # Указывает, что виджет является всплывающим окном верхнего уровня,
                                        # т.е. что он является модальным,
                                        # но имеет системную рамку окна, подходящую для всплывающих меню.
            self.ui.listWidget_Extensions.itemChanged.connect(self.slot_itemChanged)
            # self.ui.pBtn_Cancel.setVisible(False)
            # self.ui.pBtn_Ok.setVisible(False)

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    @property
    def is_filter(self):
        self.loggers.info('Start')
        return self._is_filter

    @is_filter.setter
    def is_filter(self, state):
        self.loggers.info('Start')
        self._is_filter = state

    # def btnClicked_Ok(self)-> None:
    #     """ Кнопка 'Ok'
    #         Returns: None
    #     """
    #     self.accept()

    # def btnClicked_Cancel(self)-> None:
    #     """ Кнопка 'Отмена'
    #         Returns: None
    #     """
    #     self.reject()

    def setFilters(self, filters: list):
        try:
            self.loggers.info('Start')
            self.ui.listWidget_Extensions.clear()

            newItem = QListWidgetItem("(Выделить всё)")
            newItem.setCheckState(Qt.CheckState.Checked)
            self.ui.listWidget_Extensions.insertItem(self.ui.listWidget_Extensions.count(), newItem)

            for filter in filters:
                newItem = QListWidgetItem(filter)
                newItem.setCheckState(Qt.CheckState.Checked)
                self.ui.listWidget_Extensions.insertItem(self.ui.listWidget_Extensions.count(), newItem)
            self.loggers.info('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')


    def removeFilter(self, filter: str):
        try:
            self.loggers.info('Start')
            itemsFilter = self.ui.listWidget_Extensions.findItems(filter, Qt.MatchFlag.MatchFixedString)
            if itemsFilter:
                self.ui.listWidget_Extensions.removeItemWidget(
                    self.ui.listWidget_Extensions.takeItem(
                        self.ui.listWidget_Extensions.row(itemsFilter[0])))
            self.loggers.info('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def slot_itemChanged(self, item: QListWidgetItem):
        try:
            self.loggers.info('Start')
            global_state = item.checkState()
            self.ui.listWidget_Extensions.blockSignals(True)

            if item.text() == "(Выделить всё)":
                for rowl in range(1, self.ui.listWidget_Extensions.count()):
                    self.ui.listWidget_Extensions.item(rowl).setCheckState(global_state)
            else:
                if global_state == Qt.CheckState.Checked:
                    for rowl in range(1, self.ui.listWidget_Extensions.count()):
                        if Qt.CheckState.Unchecked == self.ui.listWidget_Extensions.item(rowl).checkState():
                            global_state = Qt.CheckState.Unchecked
                            break

            self.ui.listWidget_Extensions.item(0).setCheckState(global_state)
            self.is_filter = global_state != Qt.CheckState.Checked
            self.ui.listWidget_Extensions.blockSignals(False)
            self.loggers.info('End')

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')

    def getFilters(self)->set:
        try:
            self.loggers.info('Start')
            listFilters = set()
            for rowl in range(1, self.ui.listWidget_Extensions.count()):
                if Qt.CheckState.Checked == self.ui.listWidget_Extensions.item(rowl).checkState():
                    listFilters.add(self.ui.listWidget_Extensions.item(rowl).text())

        except Exception as err:
            self.loggers.warning(f'Exception = {err}')
        self.loggers.info('End')

        return listFilters






