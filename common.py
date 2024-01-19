# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 13:05:32 2023

@author: vasilyeva
"""
import os
from PyQt5.QtWidgets import QFileDialog, QStackedWidget, QTreeView, QDialog, QLineEdit
from PyQt5.QtCore import QDir

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

    dialog:QFileDialog = QFileDialog(parent, "Выберите файлы...",  parent.cwd)
    dialog.setFilter(QDir.NoDot | QDir.NoDotDot | QDir.Hidden) # show all that shit
    dialog.setFileMode(dialog.ExistingFiles) # Это перечисление используется для указания того,
                                             # что пользователь может выбрать в диалоговом окне "Файл";
                                             # т.е. что диалоговое окно вернет, если пользователь нажмет "ОК".
                                             # Этот параметр dialog.ExistingFiles из типа QFileDialog.FileMode Имена нуля или более существующих файлов.
    dialog.setOption(dialog.DontUseNativeDialog, True) # Установка опций на dialog  Не используйте собственное диалоговое окно файла.
                                                       # По умолчанию используется собственное диалоговое окно файла,
                                                       # если вы не используете подкласс QFileDialog
                                                       # который содержит Q_OBJECT макрос или платформа
                                                       # не имеют встроенного диалогового окна требуемого вам типа.

    # по умолчанию, если каталог открыт в режиме списка файлов,
    # QFileDialog.accept() показывает содержимое этого каталога,
    # но нам нужно иметь возможность "открывать" и каталоги, как мы можем делать с файлами,
    # поэтому мы просто переопределяем `accept()` с реализацией QDialog по умолчанию,
    # которая просто вернет `dialog.selectedFiles()`
    dialog.accept = lambda: QDialog.accept(dialog)
    dialog.setViewMode(QFileDialog.Detail)

    # в неродном диалоге есть много представлений элементов,
    # но те, которые отображают фактическое содержимое, создаются внутри QStackedWidget;
    # это QTreeView и QListView, и дерево используется только тогда,
    # когда viewMode установлен на QFileDialog.Details, что не в этом случае.
    stackedWidget = dialog.findChild(QStackedWidget)
    view          = stackedWidget.findChild(QTreeView)
    view.selectionModel().selectionChanged.connect(updateText)
    lineEdit = dialog.findChild(QLineEdit)

    # очищаем содержимое строки редактирования всякий раз, когда изменяется текущий каталог
    dialog.directoryEntered.connect(lambda: lineEdit.setText(''))
    res = dialog.exec_()
    if res == QFileDialog.Rejected:
        return []
    else:
        return dialog.selectedFiles()

# =============================================================================
def scanDir_typeTableDir(res: set, folder: str):
    """ Возвращает все файлы+путь из папки (с учетом вложенных папок)

    Args:
        res (set): результат, множество файлов
        folder (str): путь к папке
    """
    for root, dirs, files in os.walk(folder, topdown=True):
        # r1 = root.replace('\\','/')
        for name in files:
            path = os.path.join(root, name).replace('\\','/')
            res.add(path)

