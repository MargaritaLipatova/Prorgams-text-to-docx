""" Тесты кнопок
"""

import pytest
from PyQt5.QtCore import  Qt, QTimer
from common import scanDir_typeTableDir
from PyQt5.QtWidgets import QFileDialog,  QTreeView
import dialog_Ishod_w

# from subprocess import Popen, PIPE
import psutil
import time
import os
# from tests.conftest import app

# from pytestqt.qt_compat import qt_api


def kill_proc_tree(qtbot, pid, including_parent=True):
    # https://stackoverflow.com/questions/1230669/subprocess-deleting-child-processes-in-windows

    # print("kill_proc_tree start")
    parent = psutil.Process(pid)
    # print(f'parent = {parent}')
    # children = parent.children()
    children = parent.children(recursive=True)
    # print(f'children  = {children }')
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
    # print("kill_proc_tree end")

def delete_file(global_data):
    """ Удаление созданных файлов программой
    """
    tmp_tmp_docx = global_data['dir_parent']+'\\~$mp_doc.docx'
    tmp_docx = global_data['dir_parent']+'\\tmp_doc.docx'
    if os.path.exists(tmp_tmp_docx):
        os.remove(tmp_tmp_docx)
    if os.path.exists(tmp_docx):
        os.remove(tmp_docx)

@pytest.fixture(scope = 'module')
def global_data():
    print('global_data start')
    return {'list_filters': [],
            "dir_parent": None,
            'res_scan_dir': set(),
            'sNameFile': 'Тестовый файл',
            'sNameDocx': 'ЯУ.0123456.012-08',
            }

@pytest.fixture
def fix_simple_run(app, qtbot, global_data):
    """Сообщает продолжительность теста после каждой функции."""
    print('\nfix_simple_run start')
    start = time.time()
    global_data['dir_parent'] = os.getcwd()
    # print(global_data['dir_parent'])

    yield app, qtbot, global_data

    # messagebox = app.findChild(QMessageBox)
    # if messagebox:
    #     print(messagebox)
    #     yes_button = messagebox.button(QMessageBox.Yes)
    #     qtbot.mouseClick(yes_button, Qt.LeftButton, delay=1)

    qtbot.wait(3000)

    # delete_file(global_data)

    stop = time.time()
    delta = stop - start
    print('\ntest duration : {:0.3} seconds'.format(delta))

@pytest.fixture
def fix_fill_name_docx_run(app, qtbot, global_data):
    """Сообщает продолжительность теста после каждой функции."""
    print('\nfix_fill_name_docx_run start')
    start = time.time()

    app.ui.lineEdit_NameFile.setText(global_data['sNameFile'])
    app.ui.lineEdit_NameDocx.setText(global_data['sNameDocx'])

    global_data['dir_parent'] = os.getcwd()
    # print(global_data['dir_parent'])

    yield app, qtbot, global_data

    qtbot.wait(3000)

    # delete_file(global_data)

    stop = time.time()
    delta = stop - start
    print('\ntest duration : {:0.3} seconds'.format(delta))

@pytest.mark.usefixtures("fix_fill_name_docx_run")
def test_line_edit(app, qtbot, global_data):
    assert app.ui.lineEdit_NameFile.text() == global_data['sNameFile']
    assert app.ui.lineEdit_NameDocx.text() == global_data['sNameDocx']

@pytest.mark.usefixtures("fix_simple_run")
def test_button_add_cancel(app, qtbot, global_data):
    """ Тестирование:
        кнопки "Добавить" и в диалоговом окне "Выбирите файлы" кнопку "Cancel"
    """
    def handle_dialog():
        dialog = next(child for child in app.children() if isinstance(child, QFileDialog))
        dialog.reject()

    QTimer.singleShot(20, handle_dialog)
    qtbot.mouseClick(app.ui.pBtn_AddFilesInFolder, Qt.LeftButton, delay=1)
    countRow = app.tvSourceCodeFiles.model().rowCount()
    assert countRow == 0


@pytest.mark.usefixtures("fix_simple_run")
def test_button_add_open(app, qtbot,global_data):
    """ Тестирование:
        кнопки "Добавить" и в диалоговом окне "Выберите файлы..." кнопку "Open"
    """
    def handle_dialog():
        dialog = next(child for child in app.children() if isinstance(child, QFileDialog))
        dialog.findChild(QTreeView).selectAll()
        dialog.accept()

    QTimer.singleShot(20, handle_dialog)
    qtbot.mouseClick(app.ui.pBtn_AddFilesInFolder, Qt.LeftButton,delay=1)

    countRow   = app.tvSourceCodeFiles.model().rowCount()
    scanDir_typeTableDir(global_data['res_scan_dir'], global_data['dir_parent'])
    # res.add(res.pop()+'s2') # это для показа ошибки
    assert len(global_data['res_scan_dir']) == countRow


@pytest.mark.usefixtures("fix_simple_run")
def test_button_preview(app, qtbot, global_data):
    """ Тест кнопки "Предпросмотр".
        Проблема теста: необходимо время для создания процесса и файла.
    """
    def handle_dialog():
        pid = app.worker.get_pid()
        if pid is not None:
            kill_proc_tree(qtbot, pid,False)

    QTimer.singleShot(2000, handle_dialog)
    qtbot.mouseClick(app.ui.pBnt_PreviewDocx, Qt.LeftButton, delay = 1)
    qtbot.wait(2000)

    tmp_docx = global_data['dir_parent']+'\\'+'tmp_doc.docx'
    assert os.path.exists(tmp_docx) == True
    # if os.path.exists(tmp_docx):
    #     os.remove(tmp_docx)

@pytest.mark.usefixtures("fix_simple_run")
def test_button_create_docx_cancel(app, qtbot, global_data):
    def handle_dialog_save():
        dialog = None
        for child in app.children():
            if isinstance(child, QFileDialog):
                if child.windowTitle() == 'Сохранение файла':
                    dialog = child
        dialog.reject()

    QTimer.singleShot(1000, handle_dialog_save)
    app.ui.lineEdit_NameDocx.setText(global_data['sNameDocx'])
    qtbot.mouseClick(app.ui.pBtn_CreateDocx, Qt.LeftButton, delay=1)
    tmp_docx = global_data['dir_parent']+'\\'+global_data['sNameDocx']+'.docx'
    assert os.path.exists(tmp_docx) is False

    qtbot.wait(1000)

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.usefixtures("fix_fill_name_docx_run")
def test_button_create_docx_save(app, qtbot, global_data):
    def handle_dialog_save():
        dialog:QFileDialog = None
        for child in app.children():
            if isinstance(child, QFileDialog):
                print(child.windowTitle())
                if child.windowTitle() == 'Сохранение файла':
                    dialog = child

        fileName = dialog.selectedFiles()
        dialog.setDirectory(fileName[0].split('/')[0])
        dialog.accept()
        # qtbot.wait(20)
        # print('handle_msg_box')
        # dialog = next(child
        #           for child in app.children()
        #           if isinstance(child, QMessageBox))
        # dialog.accept()


    try:
        print('click create_docx')
        QTimer.singleShot(1000, handle_dialog_save)
        with qtbot.capture_exceptions() as exceptions:
            qtbot.mouseClick(app.ui.pBtn_CreateDocx, Qt.LeftButton, delay = 1)
        assert len(exceptions) == 1

        print('unclick create_docx')
        tmp_docx = global_data['dir_parent']+'\\'+global_data['sNameDocx']+'.docx'
        assert os.path.exists(tmp_docx) is True
        if os.path.exists(tmp_docx):
            os.remove(tmp_docx)

    except Exception as err:
        print(f'Exception = {err}')

@pytest.mark.usefixtures("fix_fill_name_docx_run")
def test_create_docx(app, qtbot, global_data):
    def handle_dialog():
        dialog = next(child for child in app.children() if isinstance(child, QFileDialog))
        dialog.findChild(QTreeView).selectAll()
        dialog.accept()


    QTimer.singleShot(100, handle_dialog)
    qtbot.mouseClick(app.ui.pBtn_AddFilesInFolder, Qt.LeftButton)

    file = global_data['sNameDocx'] + '.docx'
    app.create_docx(file)

    is_exists = os.path.exists(file)
    assert is_exists is True

    if is_exists:
        os.remove(file)

        is_exists = os.path.exists(file)
        assert is_exists is False








