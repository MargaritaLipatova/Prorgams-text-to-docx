# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Work_Xoma\GitHub\dialogChangeExtensions.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialogChangeExtensions(object):
    def setupUi(self, dialogChangeExtensions):
        dialogChangeExtensions.setObjectName("dialogChangeExtensions")
        dialogChangeExtensions.resize(260, 154)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialogChangeExtensions)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget_Extensions = QtWidgets.QListWidget(dialogChangeExtensions)
        self.listWidget_Extensions.setObjectName("listWidget_Extensions")
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.listWidget_Extensions.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.listWidget_Extensions.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.listWidget_Extensions.addItem(item)
        self.verticalLayout.addWidget(self.listWidget_Extensions)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_Ok = QtWidgets.QPushButton(dialogChangeExtensions)
        self.pushButton_Ok.setObjectName("pushButton_Ok")
        self.horizontalLayout.addWidget(self.pushButton_Ok)
        self.pushButton_Cancel = QtWidgets.QPushButton(dialogChangeExtensions)
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.horizontalLayout.addWidget(self.pushButton_Cancel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(dialogChangeExtensions)
        QtCore.QMetaObject.connectSlotsByName(dialogChangeExtensions)

    def retranslateUi(self, dialogChangeExtensions):
        _translate = QtCore.QCoreApplication.translate
        dialogChangeExtensions.setWindowTitle(_translate("dialogChangeExtensions", "Изменить расширения..."))
        __sortingEnabled = self.listWidget_Extensions.isSortingEnabled()
        self.listWidget_Extensions.setSortingEnabled(False)
        item = self.listWidget_Extensions.item(0)
        item.setText(_translate("dialogChangeExtensions", ".cpp"))
        item = self.listWidget_Extensions.item(1)
        item.setText(_translate("dialogChangeExtensions", ".h"))
        item = self.listWidget_Extensions.item(2)
        item.setText(_translate("dialogChangeExtensions", ".hpp"))
        self.listWidget_Extensions.setSortingEnabled(__sortingEnabled)
        self.pushButton_Ok.setText(_translate("dialogChangeExtensions", "ОК"))
        self.pushButton_Cancel.setText(_translate("dialogChangeExtensions", "Отмена"))