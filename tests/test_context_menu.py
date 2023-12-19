""" Тесты контекстного меню таблицы
"""

import pytest
from PyQt5.QtCore import Qt, QTimer, QPoint
from common import scanDir_typeTableDir
from PyQt5.QtWidgets import QFileDialog,  QTreeView, QAction
import dialog_Ishod_w
import time
import os


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
    print('app start')
    test_gui_app = dialog_Ishod_w.dialogIshodDocx()
    qtbot.addWidget(test_gui_app)
    test_gui_app.show()
    return test_gui_app

@pytest.fixture(scope = 'module')
def global_data():
    print('\nglobal_data start')
    return {'list_filters': [],
            'res_scan_dir': set(),
            'dir_parent': None}


@pytest.fixture
def fix_context_menu(app, qtbot, global_data):
    """Сообщает продолжительность теста после каждой функции."""
    def handle_dialog():
        print('handle_dialog start')
        # Поиск диалогового окна
        dialog = next(child for child in app.children() if isinstance(child, QFileDialog))
        # Поиск списка для выделения
        dialog.findChild(QTreeView).selectAll()
        global_data['dir_parent'] = dialog.directory().currentPath()
        dialog.accept()

    start = time.time()

    QTimer.singleShot(100, handle_dialog)
    qtbot.mouseClick(app.ui.pBtn_AddFilesInFolder, Qt.LeftButton)

    countRow   = app.tvSourceCodeFiles.model().rowCount()
    tablefiles = app.tvSourceCodeFiles.getAllListTable()
    scanDir_typeTableDir(global_data['res_scan_dir'], global_data['dir_parent'])
    assert len(global_data['res_scan_dir']) == countRow
    assert global_data['res_scan_dir'] == tablefiles

    yield app, qtbot, global_data

    stop = time.time()
    delta = stop - start
    print('\ntest duration : {:0.3} seconds'.format(delta))

@pytest.mark.usefixtures("fix_context_menu")
def test_ctxMenu_delete(app, qtbot, global_data):
    def handle_ctx_menu():
        print('handle_ctx_menu start')

        for act in app.tvSourceCodeFiles.qMenuTable.actions():
            if act.text() == 'Удалить':
                act.trigger()

        app.tvSourceCodeFiles.qMenuTable.close()

    print('test_filter_zero start')

    app.tvSourceCodeFiles.setFocus()
    app.tvSourceCodeFiles.selectRow(0)
    after_table = app.tvSourceCodeFiles.getAllListTable()
    after_row = app.tvSourceCodeFiles.model().rowCount()
    QTimer.singleShot(100, handle_ctx_menu)
    app.tvSourceCodeFiles.ctxMenu(QPoint(11,11))
    before_table = app.tvSourceCodeFiles.getAllListTable()
    before_row = app.tvSourceCodeFiles.model().rowCount()

    assert after_table != before_table
    print(after_row, before_row)
    assert after_row != before_row


@pytest.mark.usefixtures("fix_context_menu")
def test_ctx_menu_delete_ex(app, qtbot, global_data):
    def handle_ctx_menu():
        print('handle_ctx_menu start')
        i=0
        for menu_act in app.tvSourceCodeFiles.menuDeleteFilesEx.actions():
            menu_act.trigger()
            if i == 1:
                break
            i+=1

        app.tvSourceCodeFiles.qMenuTable.close()

    print('test_filter_zero start')

    app.tvSourceCodeFiles.setFocus()
    app.tvSourceCodeFiles.selectRow(0)
    after_table = app.tvSourceCodeFiles.getAllListTable()
    after_row = app.tvSourceCodeFiles.model().rowCount()
    QTimer.singleShot(100, handle_ctx_menu)
    app.tvSourceCodeFiles.ctxMenu(QPoint(11,11))
    before_table = app.tvSourceCodeFiles.getAllListTable()
    before_row = app.tvSourceCodeFiles.model().rowCount()

    assert after_table != before_table
    print(after_row, before_row)
    assert after_row != before_row















