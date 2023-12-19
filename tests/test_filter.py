""" Тесты для фильтров таблицы
"""

import pytest
from PyQt5.QtCore import Qt, QTimer
from common import scanDir_typeTableDir
from PyQt5.QtWidgets import QFileDialog,  QTreeView
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
    print('\n')
    print('app start')
    test_gui_app = dialog_Ishod_w.dialogIshodDocx()
    qtbot.addWidget(test_gui_app)
    test_gui_app.show()
    return test_gui_app

@pytest.fixture(scope = 'module')
def global_data():
    print('global_data start')
    return {'list_filters': [],
            "dir_parent": None,
            'res_scan_dir': set(),
            }


@pytest.fixture# (autouse=True)
def fix_filter(app, qtbot, global_data):
    """Сообщает продолжительность теста после каждой функции."""
    start = time.time()
    print('\n')
    print('fix_filter start')
    def handle_dialog():
        print('handle_dialog start')
        dialog = next(child
                        for child in app.children()
                        if isinstance(child, QFileDialog))
        dialog.findChild(QTreeView).selectAll()
        global_data['dir_parent'] = dialog.directory().currentPath()
        dialog.accept()

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


@pytest.mark.usefixtures("fix_filter")
def test_filter_unchecked_all(app, qtbot, global_data):
    def handle_dialog_filter():
        # Снимается галочка "Выделить всё"
        app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(0).setCheckState(Qt.CheckState.Unchecked)
        app.tvSourceCodeFiles.dlgFilterEx.accept()

    print('test_filter_zero start')
    QTimer.singleShot(100, handle_dialog_filter)
    qtbot.mouseClick(app.tvSourceCodeFiles.filter_pBtn, Qt.LeftButton)
    qtbot.wait(1000)
    countRow = app.tvSourceCodeFiles.model().rowCount()
    assert countRow == 0

@pytest.mark.usefixtures("fix_filter")
def test_filter_change(app, qtbot, global_data):
    print('test_filter_two start')
    def handle_dialog_filter():
        # Снимается галочка "Выделить всё"
        # Устанавливается галочка на первых трёх фильтров и последнем фильтре
        count_Row = app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.count()
        global_data['list_filters'].append(app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(1).text())
        global_data['list_filters'].append(app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(count_Row-1).text())
        app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(0).setCheckState(Qt.CheckState.Unchecked)
        app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(1).setCheckState(Qt.CheckState.Checked)
        app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(count_Row-1).setCheckState(Qt.CheckState.Checked)
        app.tvSourceCodeFiles.dlgFilterEx.accept()

    QTimer.singleShot(2, handle_dialog_filter)
    qtbot.mouseClick(app.tvSourceCodeFiles.filter_pBtn, Qt.LeftButton)

    countRow = app.tvSourceCodeFiles.model().rowCount()
    listRowRes = list(path for path in global_data['res_scan_dir'] if os.path.splitext(path)[-1] in global_data['list_filters'])
    countRowRes = len(listRowRes)

    assert countRow == countRowRes















