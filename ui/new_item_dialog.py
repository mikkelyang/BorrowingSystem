# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_item_dialog.ui',
# licensing of 'new_item_dialog.ui' applies.
#
# Created: Fri Jun 14 16:07:17 2019
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 348)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        self.lbl_item_name = QtWidgets.QLabel(self.frame)
        self.lbl_item_name.setObjectName("lbl_item_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_item_name)
        self.line_item_name = QtWidgets.QLineEdit(self.frame)
        self.line_item_name.setObjectName("line_item_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.line_item_name)
        self.lbl_brand = QtWidgets.QLabel(self.frame)
        self.lbl_brand.setObjectName("lbl_brand")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_brand)
        self.line_brand = QtWidgets.QLineEdit(self.frame)
        self.line_brand.setObjectName("line_brand")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.line_brand)
        self.lbl_category = QtWidgets.QLabel(self.frame)
        self.lbl_category.setObjectName("lbl_category")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lbl_category)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.combo_category = QtWidgets.QComboBox(self.frame)
        self.combo_category.setObjectName("combo_category")
        self.horizontalLayout.addWidget(self.combo_category)
        self.btn_new_category = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_new_category.sizePolicy().hasHeightForWidth())
        self.btn_new_category.setSizePolicy(sizePolicy)
        self.btn_new_category.setObjectName("btn_new_category")
        self.horizontalLayout.addWidget(self.btn_new_category)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.lbl_item_type = QtWidgets.QLabel(self.frame)
        self.lbl_item_type.setObjectName("lbl_item_type")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lbl_item_type)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.combo_item_type = QtWidgets.QComboBox(self.frame)
        self.combo_item_type.setObjectName("combo_item_type")
        self.horizontalLayout_2.addWidget(self.combo_item_type)
        self.btn_new_item_type = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_new_item_type.sizePolicy().hasHeightForWidth())
        self.btn_new_item_type.setSizePolicy(sizePolicy)
        self.btn_new_item_type.setObjectName("btn_new_item_type")
        self.horizontalLayout_2.addWidget(self.btn_new_item_type)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.lbl_remarks = QtWidgets.QLabel(self.frame)
        self.lbl_remarks.setObjectName("lbl_remarks")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lbl_remarks)
        self.text_remarks = QtWidgets.QPlainTextEdit(self.frame)
        self.text_remarks.setObjectName("text_remarks")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.text_remarks)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "New Item", None, -1))
        self.lbl_item_name.setText(QtWidgets.QApplication.translate("Dialog", "Item Name", None, -1))
        self.lbl_brand.setText(QtWidgets.QApplication.translate("Dialog", "Brand", None, -1))
        self.lbl_category.setText(QtWidgets.QApplication.translate("Dialog", "Category", None, -1))
        self.btn_new_category.setText(QtWidgets.QApplication.translate("Dialog", "New", None, -1))
        self.lbl_item_type.setText(QtWidgets.QApplication.translate("Dialog", "Item Type", None, -1))
        self.btn_new_item_type.setText(QtWidgets.QApplication.translate("Dialog", "New", None, -1))
        self.lbl_remarks.setText(QtWidgets.QApplication.translate("Dialog", "Remarks", None, -1))

