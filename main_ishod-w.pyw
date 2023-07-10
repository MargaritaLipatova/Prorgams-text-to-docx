# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 13:18:38 2022

@author: Маргарита, Васильева
"""

import sys
from PyQt5 import QtWidgets
from dialog_Ishod_w import dialogIshodDocx

def start_main():
    app = QtWidgets.QApplication([])
    application = dialogIshodDocx()
    application.show()

    print("Start program 'ishod-w' ")
    a = app.exec()
    print("Exit program 'ishod-w' ")
    sys.exit(a)

if __name__ == "__main__":
    start_main()

