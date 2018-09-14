# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Project\pythonui\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog1")
        Dialog.resize(400, 400)
        # self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        # self.buttonBox.setGeometry(QtCore.QRect(40, 260, 341, 32))
        # self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        # self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        # self.buttonBox.setObjectName("buttonBox")
        # self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        # self.graphicsView.setGeometry(QtCore.QRect(0, 0, 401, 261))
        # self.graphicsView.setObjectName("graphicsView")

        self.retranslateUi(Dialog)
        #self.buttonBox.accepted.connect(Dialog.accept)
        #self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
