# """_summary_
# """


# # sys.path.append("../ui") # to see modules in parent's directory

# import sys
# import unittest

# from PyQt5.QtCore import Qt
# # import loggers
# # from pytestqt import qtbot
# # import conftest
# from PyQt5.QtWidgets import QApplication, QPushButton

# from dialog_Ishod_w import dialogIshodDocx

# # from pytestqt import qtbot
# # Источник: https://katerinasokol.ru/kak-ispolzovat-pytest-qt
# # import pytest
# # from pytestqt.plugin import QtBot

# app = QApplication([])
# # export QT_DEBUG_PLUGINS=1
# # app = QApplication(sys.argv) # without it we cannot test anything

# class MainWindowTest(unittest.TestCase):

#     # app = None  # hold QMainWindow in variable
#     mainwindow = None  # hold QMainWindow in variable
#     # ui = None   # hold GUI in variable

#     def setUp(self,qtbot):
#         # self.mainwindow = QMainWindow() # create empty QMainWindow
#         # self.ui = Ui_MainWindow() # we want to test GUI - only
#         # self.ui.setupUi(self.mainwindow) # set GUI for freshly created QMainWindow
#         self.mainwindow = dialogIshodDocx()        # Инициализация ui-интерфейсов
#         # self.ui.setupUi(self)                 # Установка ui-интерфейсов
#         self.mainwindow.ui.lineEdit_NameFile.setText('Тестовый файл')
#         self.mainwindow.ui.lineEdit_NameDocx.setText('ЯУ.0123456.012-08')
#         qtbot.addWidget(self.mainwindow)

#     # Check tab names of QTabWidget
#     def test_checkTabNames(self, qtbot):
#         print(qtbot)
#         # mainwindow = dialogIshodDocx()        # Инициализация ui-интерфейсов
#         # self.ui.setupUi(self)                 # Установка ui-интерфейсов
#         self.mainwindow.ui.lineEdit_NameFile.setText('Тестовый файл')
#         self.mainwindow.ui.lineEdit_NameDocx.setText('ЯУ.0123456.012-08')
# #
#         self.assertEqual(self.mainwindow.ui.lineEdit_NameFile.text(),'Тестовый файл')
#         self.assertEqual(self.mainwindow.ui.lineEdit_NameDocx.text(),'ЯУ.0123456.012-08')
#         # Отображение окна
#         self.mainwindow.show()
#         # qtbot.addWidget(self.mainwindow)
#         # Ожидание, чтобы окно успело отобразиться
#         qtbot.wait_for_window_shown(self.mainwindow)
#         # # Поиск кнопки "OK" и проверка ее отображения
#         # button = self.mainwindow.findChild(QPushButton, "Добавить...")
#         # qtbot.mouseClick(button, Qt.LeftButton)
#         # assert button.text() == "Добавить..."
#         # assert button.isVisible()
#         # Источник: https://advicemama.ru/kak-ispolzovat-pytest-qt
#         # self.assertEqual(self.ui.tabWidgetTests.tabText(1), "Renal Panel")
#         # self.assertEqual(self.ui.tabWidgetTests.tabText(2), "Liver Panel")
#         # self.assertEqual(self.ui.tabWidgetTests.tabText(3), "Thyroid Panel")
#         # self.assertEqual(self.ui.tabWidgetTests.tabText(4), "Electrolyte Panel")
#         # self.assertEqual(self.ui.tabWidgetTests.tabText(5), "Lipid Panel")

# # import pytest
# # from pytestqt import qtbot


# # def test_button_click(qtbot):

# #     button = QPushButton("Click me")
# #     widget = QWidget()
# #     layout = QVBoxLayout()
# #     layout.addWidget(button)
# #     widget.setLayout(layout)
# #     with qtbot.waitSignal(button.clicked):
# #     qtbot.mouseClick(button, Qt.LeftButton)
# #     assert button.text() == "Clicked"
# #     # Источник: https://katerinasokol.ru/kak-ispolzovat-pytest-qt

# # from PyQt5.QtWidgets import QApplication
# # from PyQt5.QtTest import QTest
# # from   PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
# # from   dialog_Ishod_w  import dialogIshodDocx
# # from   PyQt5.QtCore  import Qt
# # from   dialog_Ishod_w  import dialogIshodDocx

# # def test_button_click(self, qtbot):
# #     app = QApplication([])
# #     window = dialogIshodDocx()

# #     print(qtbot)
# #     QTest.mouseClick(window.pBtn_AddFilesInFolder, Qt.LeftButton)

# #     self.assertEqual(window.result_label.text(), "Button Clicked")

import pytest
from PyQt5.QtCore import QDir, QModelIndex, Qt, QTimer, QUrl, QThread
# import loggers
# from pytestqt import qtbot
from common import scanDir_typeTableDir
# import conftest
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QPushButton, QTableView, QTreeView

# from dialog_Ishod_w import dialogIshodDocx
import dialog_Ishod_w

# app = QApplication([])
from subprocess import Popen, PIPE

@pytest.fixture
def app(qtbot)->dialog_Ishod_w.dialogIshodDocx:
    """ Создание основного приложение и подключение к qtbot

    Args:
        qtbot (_type_): Экземпляры этого класса отвечают
        за отправку событий объектам Qt (обычно виджетам).
        Имитация пользовательского ввода.

    Returns:
        dialog_Ishod_w.dialogIshodDocx: объект основного приложения
    """
    test_gui_app = dialog_Ishod_w.dialogIshodDocx()
    qtbot.addWidget(test_gui_app)
    return test_gui_app

@pytest.fixture
def dir_parent(qtbot, app)->str:
    test_gui_app = dialog_Ishod_w.dialogIshodDocx()
    qtbot.addWidget(test_gui_app)
    return test_gui_app

def test_name(app):
    app.ui.lineEdit_NameFile.setText('Тестовый файл')
    app.ui.lineEdit_NameDocx.setText('ЯУ.0123456.012-08')

    assert app.ui.lineEdit_NameFile.text() == 'Тестовый файл'
    assert app.ui.lineEdit_NameDocx.text() == 'ЯУ.0123456.012-08'

def test_button_add_cancel_click(app, qtbot):
    """ Тестирование:
        кнопки "Добавить" и в диалоговом окне "Выбирите файлы" кнопку "Cancel"
    Args:
        app (_type_): приложение
        qtbot (_type_): _description_
    """
    def handle_dialog():
        dialog = next(child
                      for child in app.children()
                      if isinstance(child, QFileDialog))
        dialog.reject()  #still hangs

    QTimer.singleShot(200, handle_dialog)
    button = app.ui.pBtn_AddFilesInFolder
    qtbot.mouseClick(button, Qt.LeftButton, delay=1)
    countRow = app.tvSourceCodeFiles.model().rowCount()
    assert countRow == 0

def test_button_add_open_click(app, qtbot):
    """ Тестирование:
        кнопки "Добавить" и в диалоговом окне "Выберите файлы..." кнопку "Open"
    Args:
        app (_type_): приложение
        qtbot (_type_): Экземпляры этого класса отвечают за отправку событий объектам Qt (обычно виджетам), Имитация пользовательского ввода.
    """
    def handle_dialog():
        dialog = next(child
                      for child in app.children()
                      if isinstance(child, QFileDialog))
        view = dialog.findChild(QTreeView)
        view.selectAll()
        global dir_parent
        dir_parent = dialog.directory().currentPath()
        dialog.accept()

    QTimer.singleShot(200, handle_dialog)
    button = app.ui.pBtn_AddFilesInFolder
    qtbot.mouseClick(button, Qt.LeftButton, delay=1)
    countRow   = app.tvSourceCodeFiles.model().rowCount()
    tablefiles = app.tvSourceCodeFiles.getAllListTable()

    res=set()
    scanDir_typeTableDir(res, dir_parent)

    # res.add(res.pop()+'s2') # это для показа ошибки
    assert len(res) == countRow
    assert res == tablefiles

def test_button_preview(app, qtbot):
    """ Тестирование:
        кнопки "Добавить" и в диалоговом окне "Выберите файлы..." кнопку "Open"
    Args:
        app (_type_): приложение
        qtbot (_type_): Экземпляры этого класса отвечают за отправку событий объектам Qt (обычно виджетам), Имитация пользовательского ввода.
    """
    def handle_dialog():
        dialog = next(child
                      for child in app.children()
                      if isinstance(child, QFileDialog))
        view = dialog.findChild(QTreeView)
        view.selectAll()
        global dir_parent
        dir_parent = dialog.directory().currentPath()
        dialog.accept()

    def handle_dialog_1():
        dialog = None
        for child in app.children():
            # if isinstance(child, QThread):
            print(type(child))
        # app.worker.deleteLater()

        for i in Popen('tasklist', stdout=PIPE).stdout.readlines():
            print(i.decode('cp866', 'ignore'))
                # print(child)
    QTimer.singleShot(200, handle_dialog)
    button = app.ui.pBtn_AddFilesInFolder
    qtbot.mouseClick(button, Qt.LeftButton, delay=1)
    QTimer.singleShot(200, handle_dialog_1)
    button = app.ui.pBnt_PreviewDocx
    qtbot.mouseClick(button, Qt.LeftButton, delay=1)

def test_button_create_docx(app, qtbot):
    def handle_dialog_save():
        dialog = None
        for child in app.children():
            if isinstance(child, QFileDialog):
                if child.windowTitle() == 'Сохранение файла':
                    dialog = child
    #     dialog = next(child
    #                   for child in app.children()
    #                   if isinstance(child, QFileDialog))
    #     # view = dialog.findChild(QTreeView)
    #     # view.selectAll()
    #     # global dir_parent
    #     # dir_parent = dialog.directory().currentPath()
    # #     dialog.accept()
        dialog.reject()

    def handle_dialog():
        print('handle_dialog')
        dialog = next(child
                      for child in app.children()
                      if isinstance(child, QFileDialog))
        # view = dialog.findChild(QTreeView)
        # view.selectAll()
        # global dir_parent
        # dir_parent = dialog.directory().currentPath()
    #     dialog.accept()
        dialog.reject()
    # app.ui.lineEdit_NameFile.setText('Тестовый файл')
    # app.ui.lineEdit_NameDocx.setText('ЯУ.0123456.012-08')
    QTimer.singleShot(500, handle_dialog)
    button = app.ui.pBtn_AddFilesInFolder
    qtbot.mouseClick(button, Qt.LeftButton, delay=1)
    print('\n qtbot.mouseClick pBtn_AddFilesInFolder')

    QTimer.singleShot(500, handle_dialog_save)
    button = app.ui.pBtn_CreateDocx
    qtbot.mouseClick(button, Qt.LeftButton, delay=1)
    print('qtbot.mouseClick pBtn_CreateDocx')

    # countRow   = app.tvSourceCodeFiles.model().rowCount()
    # tablefiles = app.tvSourceCodeFiles.getAllListTable()

    # res=set()
    # scanDir_typeTableDir(res, dir_parent)

    # # res.add(res.pop()+'s2') # это для показа ошибки
    # assert len(res) == countRow
    # assert res == tablefiles

# def test_button_add_open_click(app, qtbot):
#     """ Тестирование:
#         кнопки "Добавить" и в диалоговом окне "Выбирите файлы" кнопку "Cancel"
#     Args:
#         app (_type_): приложение
#         qtbot (_type_): Экземпляры этого класса отвечают за отправку событий объектам Qt (обычно виджетам), Имитация пользовательского ввода.
#     """
#     def handle_dialog():
#         dialog = next(child
#                       for child in app.children()
#                       if isinstance(child, QFileDialog))
#         # parentDir = dialog.findChild(QPushButton)
#         # # parentDir = next(child for child in dialog.findChild(QPushButton) if child.tooTip()== 'Parent Directory')

#         # prntDir = dialog.findChild(QPushButton, tooltip='Parent Directory')
#         # print(parentDir)
#         # stackedWidget = dialog.findChild(QtWidgets.QStackedWidget)
#         view = dialog.findChild(QTreeView)
#         print(view)
#         view.selectAll()
#         # qLineEdit: QLineEdit = dialog.findChild(QLineEdit)
#         # print(qLineEdit)

#         # dir: QDir = dialog.directory() # print(dir.currentPath())
#         # # dialog.directoryEntered(dir)
#         # folder=f'"{dir.currentPath().split("/")[-1]}"'
#         # print(folder)
#         # qLineEdit.setText()

#         # dialog.accept()  #still hangs
#         # qtbot.mouseClick(dialog, Qt.LeftButton, delay=1)
#         # qtbot.dialog.urlSelected(QUrl(dir.currentPath()))
#         # dialog.selectUrl(QUrl(dir.currentPath()))
#         # dialog.setDirectory(str(dir.currentPath()))
#         # dir: QDir = dialog.directory() # print(dir.currentPath())
#         # print(dir)
#         dialog.accept()  #still hangs

#     #     # get a reference to the dialog and handle it here
#     QTimer.singleShot(200, handle_dialog)
#     # qtbot.mouseClick(window.browseButton, QtCore.Qt.LeftButton, delay=1)
#     # Поиск кнопки "OK" и проверка ее отображения
#     # button = app.findChild(QPushButton, "Добавить...")
#     # assert app.ui.lineEdit_NameFile.text() == 'Тестовый файл'
#     # assert app.ui.lineEdit_NameDocx.text() == 'ЯУ.0123456.012-08'

#     button = app.ui.pBtn_AddFilesInFolder
#     # print(f'button= {button}')
# # Отображение окна
#     # app.show()
#     # qtbot.addWidget(self.mainwindow)
#     # Ожидание, чтобы окно успело отобразиться
#     # qtbot.wait_for_window_shown(app)

#     # qtbot.wait_for_window_shown()
#     qtbot.mouseClick(button, Qt.LeftButton, delay=1)
#     print('4handle_dialog')
#     # print(p1)
#     # qtbot.mouseClick(app.button, QtCore.Qt.LeftButton)
#     # assert app.text_label.text() == "Changed!"
#     # table = next(
#     #         child
#     #         for child in app.children()
#     #         if isinstance(child, QTableView))

#     countRow = app.tvSourceCodeFiles.model().rowCount()
#     print(countRow)

















