# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 13:18:38 2022

@author: Маргарита
"""
# =============================================================================
# 
# import os
# import sys  # sys нужен для передачи argv в QApplication
# from PyQt5 import QtWidgets
# 
# import ishodw  # Это наш конвертированный файл дизайна
# 
# class ExampleApp(QtWidgets.QMainWindow, ishodw.Ui_Dialog):
#     def __init__(self):
#         # Это здесь нужно для доступа к переменным, методам
#         # и т.д. в файле design.py
#         super().__init__()
#         self.setupUi(self)  # Это нужно для инициализации нашего дизайна
#         self.add_src.clicked.connect(self.browse_folder)  # Выполнить функцию browse_folder
#                                                             # при нажатии кнопки
#                                                             
#     def browse_folder(self):
#         #self.scrollArea.clear()  # На случай, если в списке уже есть элементы
#         directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
#         # открыть диалог выбора директории и установить значение переменной
#         # равной пути к выбранной директории
#     
#         if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
#             for file_name in os.listdir(directory):  # для каждого файла в директории
#                 self.scrollArea.addItem(file_name)   # добавить файл в listWidget
# 
# def main():
#     app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
#     window = ExampleApp()  # Создаём объект класса ExampleApp
#     window.show()  # Показываем окно
#     app.exec_()  # и запускаем приложение
#     
#     
# if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
#     main()  # то запускаем функцию main()    
# =============================================================================

from PyQt5 import QtWidgets
from dialog_Ishod_w import dialogIshodDocx 
import sys


app = QtWidgets.QApplication([])
application = dialogIshodDocx()
application.show()

a = app.exec()
sys.exit(a)


