# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 13:18:38 2022

@author: Маргарита, Васильева
"""

import sys
from PyQt5 import QtWidgets
from dialog_Ishod_w import dialogIshodDocx
import loggers


def start_main():
    try:
        gui_loggers = loggers.get_default_logger()
        app = QtWidgets.QApplication([])
        application = dialogIshodDocx()
        application.show()

        gui_loggers.info("Start program 'ishod-w' ")
        a = app.exec()
        gui_loggers.info("Exit program 'ishod-w' ")
        sys.exit(a)

    except Exception as err:
        gui_loggers.warning(f'Exception = {err}')

if __name__ == "__main__":
    start_main()

