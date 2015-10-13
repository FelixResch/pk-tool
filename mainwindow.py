# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(734, 550)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.files_combobox = QtWidgets.QComboBox(self.centralWidget)
        self.files_combobox.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.files_combobox.setObjectName("files_combobox")
        self.horizontalLayout.addWidget(self.files_combobox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table_widget = QtWidgets.QTableWidget(self.centralWidget)
        self.table_widget.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.table_widget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.table_widget)
        self.console_output = QtWidgets.QLabel(self.centralWidget)
        self.console_output.setText("")
        self.console_output.setObjectName("console_output")
        self.verticalLayout.addWidget(self.console_output)
        self.console = QtWidgets.QLineEdit(self.centralWidget)
        self.console.setObjectName("console")
        self.verticalLayout.addWidget(self.console)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 734, 27))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_export = QtWidgets.QAction(MainWindow)
        self.action_export.setObjectName("action_export")
        self.action_new = QtWidgets.QAction(MainWindow)
        self.action_new.setObjectName("action_new")
        self.action_undo = QtWidgets.QAction(MainWindow)
        self.action_undo.setObjectName("action_undo")
        self.action_redo = QtWidgets.QAction(MainWindow)
        self.action_redo.setObjectName("action_redo")
        self.toolBar.addAction(self.action_new)
        self.toolBar.addAction(self.action_export)
        self.toolBar.addAction(self.action_undo)
        self.toolBar.addAction(self.action_redo)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PK Übungstool"))
        self.label.setText(_translate("MainWindow", "Gruppe: "))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_export.setText(_translate("MainWindow", "Exportieren"))
        self.action_new.setText(_translate("MainWindow", "Neu"))
        self.action_new.setToolTip(_translate("MainWindow", "Neu"))
        self.action_undo.setText(_translate("MainWindow", "Zurück"))
        self.action_redo.setText(_translate("MainWindow", "Vor"))

