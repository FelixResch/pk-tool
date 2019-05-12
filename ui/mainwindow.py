# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(734, 550)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.table_widget = LessonTable(self.centralWidget)
        self.table_widget.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.table_widget.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.table_widget, 1, 0, 1, 2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_3.setEnabled(False)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.console = QtWidgets.QLineEdit(self.groupBox_3)
        self.console.setObjectName("console")
        self.gridLayout_4.addWidget(self.console, 1, 1, 1, 1)
        self.console_output = QtWidgets.QLabel(self.groupBox_3)
        self.console_output.setText("")
        self.console_output.setObjectName("console_output")
        self.gridLayout_4.addWidget(self.console_output, 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.groupBox_3, 2, 0, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_2.setStyleSheet("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_group = QtWidgets.QLabel(self.groupBox_2)
        self.label_group.setObjectName("label_group")
        self.horizontalLayout.addWidget(self.label_group)
        self.group_combobox = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_combobox.sizePolicy().hasHeightForWidth())
        self.group_combobox.setSizePolicy(sizePolicy)
        self.group_combobox.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.group_combobox.setObjectName("group_combobox")
        self.horizontalLayout.addWidget(self.group_combobox)
        self.label_file = QtWidgets.QLabel(self.groupBox_2)
        self.label_file.setObjectName("label_file")
        self.horizontalLayout.addWidget(self.label_file)
        self.file_combobox = QtWidgets.QComboBox(self.groupBox_2)
        self.file_combobox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.file_combobox.setObjectName("file_combobox")
        self.horizontalLayout.addWidget(self.file_combobox)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 734, 35))
        self.menuBar.setObjectName("menuBar")
        self.menuDatei = QtWidgets.QMenu(self.menuBar)
        self.menuDatei.setEnabled(False)
        self.menuDatei.setObjectName("menuDatei")
        self.menuBearbeiten = QtWidgets.QMenu(self.menuBar)
        self.menuBearbeiten.setEnabled(False)
        self.menuBearbeiten.setObjectName("menuBearbeiten")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setEnabled(False)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menuBar)
        self.action_new = QtWidgets.QAction(MainWindow)
        self.action_new.setObjectName("action_new")
        self.action_undo = QtWidgets.QAction(MainWindow)
        self.action_undo.setObjectName("action_undo")
        self.action_redo = QtWidgets.QAction(MainWindow)
        self.action_redo.setObjectName("action_redo")
        self.action_add_student = QtWidgets.QAction(MainWindow)
        self.action_add_student.setObjectName("action_add_student")
        self.action_settings = QtWidgets.QAction(MainWindow)
        self.action_settings.setEnabled(False)
        self.action_settings.setObjectName("action_settings")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_get_email = QtWidgets.QAction(MainWindow)
        self.action_get_email.setEnabled(False)
        self.action_get_email.setObjectName("action_get_email")
        self.action_commit_and_push = QtWidgets.QAction(MainWindow)
        self.action_commit_and_push.setObjectName("action_commit_and_push")
        self.action_diagram = QtWidgets.QAction(MainWindow)
        self.action_diagram.setObjectName("action_diagram")
        self.action_groups_comparison = QtWidgets.QAction(MainWindow)
        self.action_groups_comparison.setObjectName("action_groups_comparison")
        self.action_load_test_applications = QtWidgets.QAction(MainWindow)
        self.action_load_test_applications.setObjectName("action_load_test_applications")
        self.menuDatei.addAction(self.action_new)
        self.menuDatei.addAction(self.action_settings)
        self.menuDatei.addAction(self.action_commit_and_push)
        self.menuDatei.addAction(self.action_load_test_applications)
        self.menuBearbeiten.addAction(self.action_undo)
        self.menuBearbeiten.addAction(self.action_redo)
        self.menuBearbeiten.addAction(self.action_add_student)
        self.menu.addAction(self.action_about)
        self.menuTools.addAction(self.action_get_email)
        self.menuBar.addAction(self.menuDatei.menuAction())
        self.menuBar.addAction(self.menuBearbeiten.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PK Übungstool"))
        self.table_widget.setSortingEnabled(True)
        self.label_2.setText(_translate("MainWindow", "Befehl: "))
        self.groupBox_2.setTitle(_translate("MainWindow", "Gruppenauswahl:"))
        self.label_group.setText(_translate("MainWindow", "Gruppe:"))
        self.label_file.setText(_translate("MainWindow", "Übung:"))
        self.menuDatei.setTitle(_translate("MainWindow", "&Datei"))
        self.menuBearbeiten.setTitle(_translate("MainWindow", "&Bearbeiten"))
        self.menu.setTitle(_translate("MainWindow", "?"))
        self.menuTools.setTitle(_translate("MainWindow", "Too&ls"))
        self.action_new.setText(_translate("MainWindow", "&Neu"))
        self.action_new.setToolTip(_translate("MainWindow", "Neu"))
        self.action_undo.setText(_translate("MainWindow", "&Zurück"))
        self.action_redo.setText(_translate("MainWindow", "&Vor"))
        self.action_add_student.setText(_translate("MainWindow", "&Student hinzufügen"))
        self.action_settings.setText(_translate("MainWindow", "&Einstellungen"))
        self.action_about.setText(_translate("MainWindow", "&About"))
        self.action_get_email.setText(_translate("MainWindow", "&Kopiere E-Mails in die Zwischenablage"))
        self.action_commit_and_push.setText(_translate("MainWindow", "&Commit und Push"))
        self.action_diagram.setText(_translate("MainWindow", "&Gruppen-Diagramm"))
        self.action_groups_comparison.setText(_translate("MainWindow", "Gruppen-&Vergleich"))
        self.action_load_test_applications.setText(_translate("MainWindow", "&Lade Test-Anmeldungen"))
        self.action_load_test_applications.setToolTip(_translate("MainWindow", "Lade Test-Anmeldungen"))


from src.lessontable import LessonTable


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
