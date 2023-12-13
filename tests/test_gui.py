# """_summary_
# """

import pytest
import unittest
from PyQt5.QtCore import QDir, QModelIndex, Qt, QTimer, QUrl, QThread
from common import scanDir_typeTableDir
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QPushButton, QTableView, QTreeView, QDialog, QMessageBox
import dialog_Ishod_w

# from subprocess import Popen, PIPE
import subprocess
import psutil
import time
import os
import signal


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


def delete_file():
    tmp_tmp_docx = dir_parent+'\\~$mp_doc.docx'
    tmp_docx = dir_parent+'\\tmp_doc.docx'
    if os.path.exists(tmp_tmp_docx):
        os.remove(tmp_tmp_docx)
    if os.path.exists(tmp_docx):
        os.remove(tmp_docx)

@pytest.fixture#(autouse=True)
def start_func_version_1(app, qtbot):
    """Сообщает продолжительность теста после каждой функции."""
    print(start_func_version_1.__name__)
    start = time.time()

    global dir_parent
    dir_parent = os.getcwd()
    print(dir_parent)

    yield

    delete_file()

    stop = time.time()
    delta = stop - start
    print('\ntest duration : {:0.3} seconds'.format(delta))

@pytest.fixture#(autouse=True)
def start_func_version_2(app, qtbot):
    """Сообщает продолжительность теста после каждой функции."""
    print(start_func_version_2.__name__)
    start = time.time()

    global sNameFile, sNameDocx
    sNameFile, sNameDocx = 'Тестовый файл', 'ЯУ.0123456.012-08'
    app.ui.lineEdit_NameFile.setText(sNameFile)
    app.ui.lineEdit_NameDocx.setText(sNameDocx)

    global dir_parent
    dir_parent = os.getcwd()
    print(dir_parent)

    yield

    delete_file()

    stop = time.time()
    delta = stop - start
    print('\ntest duration : {:0.3} seconds'.format(delta))

@pytest.mark.usefixtures("start_func_version_2")
def test_line_edit(app):

    assert app.ui.lineEdit_NameFile.text() == 'Тестовый файл'
    assert app.ui.lineEdit_NameDocx.text() == 'ЯУ.0123456.012-08'

@pytest.mark.usefixtures("start_func_version_1")
def test_button_add_cancel_click(app, qtbot):
    """ Тестирование:
        кнопки "Добавить" и в диалоговом окне "Выбирите файлы" кнопку "Cancel"
    Args:
        app (_type_): приложение
        qtbot (_type_): _description_
    """
    def handle_dialog():
        dialog = next(child for child in app.children() if isinstance(child, QFileDialog))
        dialog.reject()  #still hangs

    QTimer.singleShot(20, handle_dialog)
    qtbot.mouseClick(app.ui.pBtn_AddFilesInFolder, Qt.LeftButton, delay=1)
    countRow = app.tvSourceCodeFiles.model().rowCount()
    assert countRow == 0

@pytest.mark.usefixtures("start_func_version_1")
def test_button_add_open_click(app, qtbot):
    """ Тестирование:
        кнопки "Добавить" и в диалоговом окне "Выберите файлы..." кнопку "Open"
    Args:
        app (_type_): приложение
        qtbot (_type_): Экземпляры этого класса отвечают за отправку событий объектам Qt (обычно виджетам), Имитация пользовательского ввода.
    """
    def handle_dialog():
        dialog = next(child for child in app.children() if isinstance(child, QFileDialog))
        view = dialog.findChild(QTreeView)
        view.selectAll()
        dialog.accept()
        time.sleep(1)

    QTimer.singleShot(20, handle_dialog)
    button = app.ui.pBtn_AddFilesInFolder
    qtbot.mouseClick(button, Qt.LeftButton, delay=1)
    time.sleep(1)
    countRow   = app.tvSourceCodeFiles.model().rowCount()
    tablefiles = app.tvSourceCodeFiles.getAllListTable()

    res=set()
    scanDir_typeTableDir(res, dir_parent)

    # res.add(res.pop()+'s2') # это для показа ошибки
    assert len(res) == countRow
    assert res == tablefiles

def kill_proc_tree(pid, including_parent=True):
    # https://stackoverflow.com/questions/1230669/subprocess-deleting-child-processes-in-windows
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        # print(child.pid)
        # print(child.name())
        if child.name() =='WINWORD.EXE':
            child.kill()
            break
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)

# @pytest.mark.disable_autouse
@pytest.mark.usefixtures("start_func_version_1")
def test_button_preview(app, qtbot):
    """ Тестирование:
        кнопки "Добавить" и в диалоговом окне "Выберите файлы..." кнопку "Open"
    Args:
        app (_type_): приложение
        qtbot (_type_): Экземпляры этого класса отвечают за отправку событий объектам Qt (обычно виджетам), Имитация пользовательского ввода.
    """
    def handle_dialog_1():
        pid = app.worker.get_pid()
        if pid is not None:
            kill_proc_tree(pid,False)

    QTimer.singleShot(20, handle_dialog_1)
    qtbot.mouseClick(app.ui.pBnt_PreviewDocx, Qt.LeftButton, delay = 1)
    time.sleep(2)

# @pytest.mark.disable_autouse
@pytest.mark.usefixtures("start_func_version_1")
def test_button_create_docx_cancel(app, qtbot):
    def handle_dialog_save():
        dialog = None
        for child in app.children():
            if isinstance(child, QFileDialog):
                if child.windowTitle() == 'Сохранение файла':
                    dialog = child
        dialog.reject()

    QTimer.singleShot(10, handle_dialog_save)
    qtbot.mouseClick(app.ui.pBtn_CreateDocx, Qt.LeftButton, delay=1)
    time.sleep(2)

# @pytest.mark.disable_autouse
@pytest.mark.usefixtures("start_func_version_2")
def test_button_create_docx_save(app, qtbot):
    def handle_dialog_save():
        try:
            print('handle_dialog_save')
            # time.sleep(2)
            dialog:QFileDialog = None
            for child in app.children():
                if isinstance(child, QFileDialog):
                    print(child.windowTitle())
                    if child.windowTitle() == 'Сохранение файла':
                        dialog = child

            print(dialog.directory().currentPath())
            fileName = dialog.selectedFiles()
            dialog.setDirectory(fileName[0].split('/')[0])
            dialog.accept()
            # time.sleep(20)
            # print('handle_msg_box')
            # dialog = next(child
            #           for child in app.children()
            #           if isinstance(child, QMessageBox))
            # dialog.accept()

        except Exception as err:
            print(f'Exception = {err}')

    try:
        QTimer.singleShot(100, handle_dialog_save)
        qtbot.mouseClick(app.ui.pBtn_CreateDocx, Qt.LeftButton)
        # QTimer.singleShot(1, handle_msg_box)
        # time.sleep(1)

    except Exception as err:
        print(f'Exception = {err}')



# @pytest.mark.disable_autouse
@pytest.mark.usefixtures("start_func_version_2")
def test_button_create_docx_save_2(app, qtbot):
    try:
        # app.ui.lineEdit_NameFile.setText('456789')
        # app.ui.lineEdit_NameDocx.setText('ЯУ.01234560.0-08')


        file = sNameDocx+'.docx'
        app.create_docx(file)

        is_exists = os.path.exists(file)
        assert is_exists == True , "11111111111111"

        if is_exists:
            os.remove(file)

            is_exists = os.path.exists(file)
            assert is_exists == False

    except Exception as err:
        print(f'Exception = {err}')

# @pytest.mark.disable_autouse
@pytest.mark.usefixtures("start_func_version_2")
def test_button_create_docx_save_3(app, qtbot):
    def handle_dialog():
        dialog = next(child
                      for child in app.children()
                      if isinstance(child, QFileDialog))
        view = dialog.findChild(QTreeView)
        view.selectAll()
        # global dir_parent
        # dir_parent = dialog.directory().currentPath()
        dialog.accept()
        time.sleep(1)

    try:
        # app.ui.lineEdit_NameFile.setText('456789')
        # app.ui.lineEdit_NameDocx.setText('ЯУ.01234560.0-08')

        QTimer.singleShot(100, handle_dialog)
        qtbot.mouseClick(app.ui.pBtn_AddFilesInFolder, Qt.LeftButton)

        file = dir_parent + '.docx'
        # file = dir_parent+'/'+'ЯУ.01234560.0-08.docx'
        app.create_docx(file)

        is_exists = os.path.exists(file)
        assert is_exists == True

        if is_exists:
            os.remove(file)

            is_exists = os.path.exists(file)
            assert is_exists == False

    except Exception as err:
        print(f'Exception = {err}')








