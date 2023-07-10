# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 13:05:32 2023

@author: vasilyeva
"""
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# =============================================================================
# from enum import Enum
# from enum import auto
#
# class typeSelection(Enum):
#     File = auto()
#     Dir  = auto()
#
# =============================================================================

# ==================================================================
# ==================================================================
# ==================================================================
# class optionsFile():
#     def __init__(self, pathFile, fileEx, stateHidden):
#         self._pathFile = pathFile
#         self._fileEx = fileEx
#         self._hiddenFile = stateHidden

#     @property
#     def pathFile(self):
#         return self._pathFile

#     @pathFile.setter
#     def pathFile(self, path):
#         self._pathFile = path

#     @property
#     def fileEx(self):
#         return self._fileEx

#     @fileEx.setter
#     def fileEx(self, ex):
#         self._fileEx = ex

#     @property
#     def stateHidden(self):
#         return self._hiddenFile

#     @stateHidden.setter
#     def stateHidden(self, state):
#         self._hiddenFile = state

class tableDir():
    def __init__(self, pathDir):
        self._pathDir = pathDir
        self._pathFiles = []
        self._checkboxDir = False

    @property
    def checkboxDir(self):
        return self._checkboxDir

    @checkboxDir.setter
    def checkboxDir(self, checkState):
        self._checkboxDir = checkState

    @property
    def pathDir(self):
        return self._pathDir
    @pathDir.setter
    def pathDir(self, pathDir):
        self._pathDir = pathDir

    @property
    def pathFiles(self):
        return self._pathFiles

    @pathFiles.setter
    def pathFiles(self, pathFiles):
        for path in pathFiles:
            if not self._pathFiles.isExsists(path):
                self._pathFiles.append(path)

    def setPathFile(self, pathFile):
        if next(filter(lambda x: pathFile in x.keys(), self._pathFiles),None) == None:
            self._pathFiles.append({pathFile: True})

    def clearPathFiles(self):
        self._pathFiles.clear()
        self._pathDir.clear()




# ==================================================================
# ==================================================================
# ==================================================================
def getOpenFilesAndDirs(parent=None, caption='', directory='', filter='', initialFilter='', options=None):
    def updateText():
        # обновить содержимое виджета редактирования строки выбранными файлами
        selected = []
        for index in view.selectionModel().selectedRows():
            selected.append('"{}"'.format(index.data()))
        lineEdit.setText(' '.join(selected))

    dialog = QtWidgets.QFileDialog(parent,
                                   "Выберите файлы...", # Название открытого QFileDialog
                                   parent.cwd)           # Начальный путь

    dialog.setFileMode(dialog.ExistingFiles) # Это перечисление используется для указания того,
                                             # что пользователь может выбрать в диалоговом окне "Файл";
                                             # т.е. что диалоговое окно вернет, если пользователь нажмет "ОК".
                                             # Этот параметр dialog.ExistingFiles из типа QFileDialog.FileMode Имена нуля или более существующих файлов.
    # if options:
        # dialog.setOptions(options)
    dialog.setOption(dialog.DontUseNativeDialog, True) #!!! # Установка опций на dialog  Не используйте собственное диалоговое окно файла. По умолчанию используется собственное диалоговое окно файла, если вы не используете подкласс QFileDialog который содержит Q_OBJECT макрос или платформа не имеют встроенного диалогового окна требуемого вам типа.

    # if directory:

    #     dialog.setDirectory(directory)
    # if filter:
    #     dialog.setNameFilter(filter)
    #     if initialFilter:
    #         dialog.selectNameFilter(initialFilter)

    # по умолчанию, если каталог открыт в режиме списка файлов,
    # QFileDialog.accept() показывает содержимое этого каталога,
    # но нам нужно иметь возможность "открывать" и каталоги, как мы можем делать с файлами,
    # поэтому мы просто переопределяем `accept()` с реализацией QDialog по умолчанию,
    # которая просто вернет `dialog.selectedFiles()`

    dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)

    dialog.setViewMode(QFileDialog.Detail)

    # в неродном диалоге есть много представлений элементов,
    # но те, которые отображают фактическое содержимое, создаются внутри QStackedWidget;
    # это QTreeView и QListView, и дерево используется только тогда,
    # когда viewMode установлен на QFileDialog.Details, что не в этом случае.

    stackedWidget = dialog.findChild(QtWidgets.QStackedWidget)
    view = stackedWidget.findChild(QtWidgets.QTreeView)
    #view = stackedWidget.findChild(QtWidgets.QListView)
    view.selectionModel().selectionChanged.connect(updateText)

    lineEdit = dialog.findChild(QtWidgets.QLineEdit)
    # очищаем содержимое строки редактирования всякий раз, когда изменяется текущий каталог
    dialog.directoryEntered.connect(lambda: lineEdit.setText(''))
    dialog.exec_()
    return dialog.selectedFiles()

# =============================================================================
def scanDir_typeTableDir(res: set, folder):
    for root, dirs, files in os.walk(folder, topdown=True):
        r1 = root.replace('\\','/')
        for name in files:
            path = os.path.join(root, name).replace('\\','/')
            res.add(path)

# =============================================================================
def scanDir(res: list, folder):
    for root, dirs, files in os.walk(folder, topdown=True):
    # for root, dirs, files in os.walk(folder, topdown=False):
        # print(root)
        for name in files:
            path = os.path.join(root, name).replace('\\','/')
            # print(path)
            res.append(path)
# =============================================================================
#             if os.path.isdir(path):
#                 scanDir(res, path)
# =============================================================================

def scanDir_nesting(folders: list)->list:
    res = []
    # print(folders)
    folders.sort()
    # print(folders)

    if folders:
        for name in folders:
            res.append(name)
            if os.path.isdir(name):
                scanDir(res, name)

    return res
