# """_summary_
# """

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
    test_gui_app = dialog_Ishod_w.dialogIshodDocx()
    qtbot.addWidget(test_gui_app)
    return test_gui_app

@pytest.fixture(autouse=True)
def footer_function_scope(app, qtbot):
    """Сообщает продолжительность теста после каждой функции."""
    start = time.time()
    print('first_action')
    def handle_dialog():
        print('handle_dialog')
        dialog = next(child
                        for child in app.children()
                        if isinstance(child, QFileDialog))
        view = dialog.findChild(QTreeView)
        view.selectAll()
        global dir_parent
        dir_parent = dialog.directory().currentPath()
        dialog.accept()
    QTimer.singleShot(100, handle_dialog)
    qtbot.mouseClick(app.ui.pBtn_AddFilesInFolder, Qt.LeftButton)
    countRow   = app.tvSourceCodeFiles.model().rowCount()
    tablefiles = app.tvSourceCodeFiles.getAllListTable()
    global res
    res=set()
    scanDir_typeTableDir(res, dir_parent)
    assert len(res) == countRow
    assert res == tablefiles

    yield

    stop = time.time()
    delta = stop - start
    print('\ntest duration : {:0.3} seconds'.format(delta))


def test_filter_zero(app, qtbot):
    print('test_filter_zero')
    def handle_dialog_filter():
        print('handle_dialog_filter')
        # Снимается галочка "Выделить всё"
        app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(0).setCheckState(Qt.CheckState.Unchecked)
        app.tvSourceCodeFiles.dlgFilterEx.accept()

    QTimer.singleShot(100, handle_dialog_filter)
    qtbot.mouseClick(app.tvSourceCodeFiles.filter_pBtn, Qt.LeftButton)

    countRow = app.tvSourceCodeFiles.model().rowCount()
    assert countRow == 0

def test_filter_two(app, qtbot):
    print('test_filter_two')
    def handle_dialog_filter():
        print('handle_dialog_filter')
        # Снимается галочка "Выделить всё"
        # Устанавливается галочка на первых трёх фильтров и последнем фильтре
        count_Row = app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.count()
        global list_filters
        list_filters = []
        list_filters.append(app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(1).text())
        list_filters.append(app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(count_Row-1).text())
        app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(0).setCheckState(Qt.CheckState.Unchecked)
        app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(1).setCheckState(Qt.CheckState.Checked)
        app.tvSourceCodeFiles.dlgFilterEx.ui.listWidget_Extensions.item(count_Row-1).setCheckState(Qt.CheckState.Checked)
        print(list_filters)
        app.tvSourceCodeFiles.dlgFilterEx.accept()

    QTimer.singleShot(100, handle_dialog_filter)
    qtbot.mouseClick(app.tvSourceCodeFiles.filter_pBtn, Qt.LeftButton)

    countRow = app.tvSourceCodeFiles.model().rowCount()
    listRowRes = list(path for path in res if os.path.splitext(path)[-1] in list_filters)
    countRowRes = len(listRowRes)
    # listRow = list()
    # for row in range(countRow):
    #     listRow.append(app.tvSourceCodeFiles.model().index(row, 0, app.tvSourceCodeFiles.rootIndex()).data(Qt.ToolTipRole)) #  # for column 0

    assert countRow == countRowRes















