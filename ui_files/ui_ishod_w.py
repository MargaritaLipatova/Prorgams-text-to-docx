# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ishod_w.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogIshodDocx(object):
    def setupUi(self, DialogIshodDocx):
        DialogIshodDocx.setObjectName("DialogIshodDocx")
        DialogIshodDocx.resize(617, 576)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        DialogIshodDocx.setFont(font)
        DialogIshodDocx.setWindowTitle("Исход-В")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DialogIshodDocx)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_NameFile = QtWidgets.QLabel(DialogIshodDocx)
        self.label_NameFile.setMinimumSize(QtCore.QSize(217, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_NameFile.setFont(font)
        self.label_NameFile.setObjectName("label_NameFile")
        self.horizontalLayout_3.addWidget(self.label_NameFile)
        self.lineEdit_NameFile = QtWidgets.QLineEdit(DialogIshodDocx)
        self.lineEdit_NameFile.setObjectName("lineEdit_NameFile")
        self.horizontalLayout_3.addWidget(self.lineEdit_NameFile)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_NameDocx = QtWidgets.QLabel(DialogIshodDocx)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_NameDocx.setFont(font)
        self.label_NameDocx.setObjectName("label_NameDocx")
        self.horizontalLayout_4.addWidget(self.label_NameDocx)
        self.lineEdit_NameDocx = QtWidgets.QLineEdit(DialogIshodDocx)
        self.lineEdit_NameDocx.setObjectName("lineEdit_NameDocx")
        self.horizontalLayout_4.addWidget(self.lineEdit_NameDocx)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.groupBox_IshodCode = QtWidgets.QGroupBox(DialogIshodDocx)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.groupBox_IshodCode.setFont(font)
        self.groupBox_IshodCode.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_IshodCode.setObjectName("groupBox_IshodCode")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_IshodCode)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView_FileTree = QtWidgets.QTableView(self.groupBox_IshodCode)
        self.tableView_FileTree.setObjectName("tableView_FileTree")
        self.verticalLayout.addWidget(self.tableView_FileTree)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.wStatusExtensions = QtWidgets.QWidget(self.groupBox_IshodCode)
        self.wStatusExtensions.setObjectName("wStatusExtensions")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.wStatusExtensions)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_Extensions = QtWidgets.QLabel(self.wStatusExtensions)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_Extensions.setFont(font)
        self.label_Extensions.setObjectName("label_Extensions")
        self.horizontalLayout_7.addWidget(self.label_Extensions)
        self.label_changeEx = QtWidgets.QLabel(self.wStatusExtensions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_changeEx.sizePolicy().hasHeightForWidth())
        self.label_changeEx.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_changeEx.setFont(font)
        self.label_changeEx.setObjectName("label_changeEx")
        self.horizontalLayout_7.addWidget(self.label_changeEx)
        self.horizontalLayout.addWidget(self.wStatusExtensions)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pBtn_ChangeEx = QtWidgets.QPushButton(self.groupBox_IshodCode)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBtn_ChangeEx.setFont(font)
        self.pBtn_ChangeEx.setObjectName("pBtn_ChangeEx")
        self.horizontalLayout.addWidget(self.pBtn_ChangeEx)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.checkBox_FolderNesting = QtWidgets.QCheckBox(self.groupBox_IshodCode)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_FolderNesting.setFont(font)
        self.checkBox_FolderNesting.setObjectName("checkBox_FolderNesting")
        self.horizontalLayout_2.addWidget(self.checkBox_FolderNesting)
        self.pBtn_AddFilesInFolder = QtWidgets.QPushButton(self.groupBox_IshodCode)
        self.pBtn_AddFilesInFolder.setMinimumSize(QtCore.QSize(140, 0))
        self.pBtn_AddFilesInFolder.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBtn_AddFilesInFolder.setFont(font)
        self.pBtn_AddFilesInFolder.setObjectName("pBtn_AddFilesInFolder")
        self.horizontalLayout_2.addWidget(self.pBtn_AddFilesInFolder)
        self.pBtn_UpdateTable = QtWidgets.QPushButton(self.groupBox_IshodCode)
        self.pBtn_UpdateTable.setMinimumSize(QtCore.QSize(25, 0))
        self.pBtn_UpdateTable.setMaximumSize(QtCore.QSize(25, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pBtn_UpdateTable.setFont(font)
        self.pBtn_UpdateTable.setWhatsThis("")
        self.pBtn_UpdateTable.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/folder_refresh_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pBtn_UpdateTable.setIcon(icon)
        self.pBtn_UpdateTable.setObjectName("pBtn_UpdateTable")
        self.horizontalLayout_2.addWidget(self.pBtn_UpdateTable)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_IshodCode)
        self.pushButton.setMinimumSize(QtCore.QSize(172, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(172, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addWidget(self.groupBox_IshodCode)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.wStatusPathSavingDocx = QtWidgets.QWidget(DialogIshodDocx)
        self.wStatusPathSavingDocx.setObjectName("wStatusPathSavingDocx")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.wStatusPathSavingDocx)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_PathIshodDocx = QtWidgets.QLabel(self.wStatusPathSavingDocx)
        self.label_PathIshodDocx.setMinimumSize(QtCore.QSize(35, 23))
        self.label_PathIshodDocx.setMaximumSize(QtCore.QSize(35, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_PathIshodDocx.setFont(font)
        self.label_PathIshodDocx.setObjectName("label_PathIshodDocx")
        self.horizontalLayout_9.addWidget(self.label_PathIshodDocx)
        self.label_PathSavingDocx = QtWidgets.QLabel(self.wStatusPathSavingDocx)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_PathSavingDocx.setFont(font)
        self.label_PathSavingDocx.setText("")
        self.label_PathSavingDocx.setObjectName("label_PathSavingDocx")
        self.horizontalLayout_9.addWidget(self.label_PathSavingDocx)
        self.horizontalLayout_5.addWidget(self.wStatusPathSavingDocx)
        self.pBtn_CreateDocx = QtWidgets.QPushButton(DialogIshodDocx)
        self.pBtn_CreateDocx.setMinimumSize(QtCore.QSize(149, 0))
        self.pBtn_CreateDocx.setMaximumSize(QtCore.QSize(185, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pBtn_CreateDocx.setFont(font)
        self.pBtn_CreateDocx.setObjectName("pBtn_CreateDocx")
        self.horizontalLayout_5.addWidget(self.pBtn_CreateDocx)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.retranslateUi(DialogIshodDocx)
        QtCore.QMetaObject.connectSlotsByName(DialogIshodDocx)

    def retranslateUi(self, DialogIshodDocx):
        _translate = QtCore.QCoreApplication.translate
        self.label_NameFile.setText(_translate("DialogIshodDocx", "Название документа"))
        self.label_NameDocx.setText(_translate("DialogIshodDocx", "Децимальный номер документа"))
        self.groupBox_IshodCode.setTitle(_translate("DialogIshodDocx", "Файлы исходных кодов"))
        self.label_Extensions.setText(_translate("DialogIshodDocx", "Расширения:"))
        self.label_changeEx.setText(_translate("DialogIshodDocx", "..."))
        self.pBtn_ChangeEx.setText(_translate("DialogIshodDocx", "Изменить расширения..."))
        self.checkBox_FolderNesting.setText(_translate("DialogIshodDocx", "с учётом вложенных папок"))
        self.pBtn_AddFilesInFolder.setText(_translate("DialogIshodDocx", "Добавить файлы..."))
        self.pBtn_UpdateTable.setToolTip(_translate("DialogIshodDocx", "Обновить таблицу"))
        self.pushButton.setText(_translate("DialogIshodDocx", "Предпросмотр"))
        self.label_PathIshodDocx.setText(_translate("DialogIshodDocx", "Путь"))
        self.pBtn_CreateDocx.setText(_translate("DialogIshodDocx", "Создать документ..."))

import resources_rc
