

import pytest
import dialog_Ishod_w



@pytest.fixture#(scope='session')
def app(qtbot)->dialog_Ishod_w.dialogIshodDocx:
    """ Создание основного приложение и подключение к qtbot

    Args:
        qtbot (_type_): Экземпляры этого класса отвечают
        за отправку событий объектам Qt (обычно виджетам).
        Имитация пользовательского ввода.

    Returns:
        dialog_Ishod_w.dialogIshodDocx: объект основного приложения
    """
    print('\napp start')
    test_gui_app = dialog_Ishod_w.dialogIshodDocx()
    qtbot.addWidget(test_gui_app)
    test_gui_app.show()
    return test_gui_app