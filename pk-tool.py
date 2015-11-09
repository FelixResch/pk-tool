import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QCheckBox, QWidget, QHBoxLayout, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from mainwindow import Ui_MainWindow
import os
import re
import io
from collections import namedtuple
from _datetime import datetime


Group = namedtuple('Group', 'day name type students')
Student = namedtuple('Student', 'name matrikelnr email')


class PkToolMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.name_files = []
        self.history_files = []
        self.history_index = None

        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        pk_repo_path = self.settings.value('Path/pk_repo', '')
        self.line_edit_repo_path.setText(pk_repo_path)
        if pk_repo_path:
            self.read_group_files()

        # self.find_files()
        # self.current_group_idx = 0
        # self.write_lock = False
        # if self.name_files:
        #     self.open_file(0)
        # else:
        #     QMessageBox().about(self, 'Keine Teilnehmerlisten gefunden',
        #                         '\n'.join(['Um das Programm verwenden zu können, müssen Sie zuerst die Teilnehmerlisten',
        #                                    'von Tuwel downloaden und in dieses Verzeichnis kopieren. Die findet man unter',
        #                                    '"Programmkonstruktion - Anmeldungen - Übungsanmeldung (Normale Gruppen) - Teilnehmer/innen". ',
        #                                    'Dort bei den jeweiligen Gruppen die .txt (z.B. 185.A79...Überblick.txt) nehmen.']))
        #
        # self.group_combobox.currentIndexChanged.connect(self.open_file)
        # self.action_export.triggered.connect(lambda: self.write_file(savefile=False))
        # self.table_widget.cellChanged.connect(lambda: self.write_file(savefile=True))
        # self.console.returnPressed.connect(self.execute_console)
        # self.action_new.triggered.connect(lambda: self.open_file(self.group_combobox.currentIndex(), new=True))
        # self.action_undo.triggered.connect(self.history_undo)
        # self.action_redo.triggered.connect(self.history_redo)
        # self.action_add_student.triggered.connect(self.add_row)
        self.button_select_repo_path.clicked.connect(self.select_repo_path)
        self.group_type_combobox.currentIndexChanged.connect(self.fill_group_names_combobox)
        self.group_day_combobox.currentIndexChanged.connect(self.fill_group_names_combobox)

    def read_group_files(self):
        path_template = self.line_edit_repo_path.text() + '/Anwesenheiten/Anmeldung/groups_{group_type}.txt'
        self.groups = []

        for group_type in 'fortgeschritten', 'normal':
            with open(path_template.format(group_type=group_type), 'r', encoding='utf-8') as f:
                group_name_regex = re.compile('(mo|di|mi|do|fr)\d{2}\w')
                student_regex = re.compile('\s+[+✔]\s+(\D+)\s(\d+)\s(.*)\s?')

                students = []
                group_name = ''

                for line in f:
                    group_name_match = group_name_regex.search(line)
                    students_match = student_regex.search(line)

                    if group_name_match:
                        if students:
                            self.groups.append(Group(group_name[:2], group_name[2:], group_type, students))
                            students = []
                        group_name = group_name_match.group(0)
                    elif students_match:
                        students.append(Student(*(students_match.group(i) for i in range(1, 4))))

            if students:
                self.groups.append(Group(group_name[:2], group_name[2:], group_type, students))

        self.group_type_combobox.addItems('Alle Normal Fortgeschritten'.split())
        self.group_day_combobox.addItems('mo di mi do fr'.split())
        self.fill_group_names_combobox()

    def fill_group_names_combobox(self):
        type_index = self.group_type_combobox.currentIndex()
        allowed_types = []
        if type_index != 1:
            allowed_types.append('fortgeschritten')
        if type_index != 2:
            allowed_types.append('normal')

        group_names = [group.name for group in self.groups
                  if group.type in allowed_types and group.day == self.group_day_combobox.currentText()]
        self.group_combobox.clear()
        self.group_combobox.addItems(group_names)

    def load_group_data(self):
        pass

    def select_repo_path(self):
        pk_repo_path = QFileDialog.getExistingDirectory(self, 'Pfad zum PK-Repository', self.line_edit_repo_path.text(), QFileDialog.ShowDirsOnly)
        if pk_repo_path:
            self.settings.setValue('Path/pk_repo', pk_repo_path)
            self.line_edit_repo_path.setText(pk_repo_path)

    def find_files(self):
        r = re.compile('185\.A79 Programmkonstruktion .*_(.*?)_Überblick.txt')
        matches = [r.search(f) for f in os.listdir('.')]
        self.name_files = [m.group(0) for m in matches if m]
        shortcuts = [m.group(1) for m in matches if m]
        self.group_combobox.addItems(shortcuts)

    def attendance_changed(self):
        self.write_file(savefile=True)
        count = sum(self.get_checkbox(index).isChecked() for index in range(self.table_widget.rowCount()))
        attendance = 'Anwesend {}/{}'.format(count, self.table_widget.rowCount())
        self.table_widget.setHorizontalHeaderItem(3, QTableWidgetItem(attendance))

    def add_row(self, student=None):
        if not student:
            self.write_lock = True

        idx = self.table_widget.rowCount()
        self.table_widget.setRowCount(idx + 1)

        if student:
            name_item = QTableWidgetItem(student.name)
            name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemIsEditable)
        else:
            name_item = QTableWidgetItem()
        self.table_widget.setItem(idx, 0, name_item)

        if student:
            matrikelnr_item = QTableWidgetItem(student.matrikelnr)
            matrikelnr_item.setFlags(matrikelnr_item.flags() & ~QtCore.Qt.ItemIsEditable)
        else:
            matrikelnr_item = QTableWidgetItem()
        matrikelnr_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 1, matrikelnr_item)

        if student:
            group_item = QTableWidgetItem(self.group_combobox.currentText())
            group_item.setFlags(matrikelnr_item.flags() & ~QtCore.Qt.ItemIsEditable)
        else:
            group_item = QTableWidgetItem()
        group_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 2, group_item)

        check_item = QTableWidgetItem()
        check_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 3, check_item)
        check_widget = QWidget()
        chk_bx = QCheckBox()
        chk_bx.setCheckState(QtCore.Qt.Unchecked)
        chk_bx.stateChanged.connect(self.attendance_changed)
        chk_bx.clicked.connect(self.update_checkbox_data)
        lay_out = QHBoxLayout(check_widget)
        lay_out.addWidget(chk_bx)
        lay_out.setAlignment(QtCore.Qt.AlignCenter)
        lay_out.setContentsMargins(0,0,0,0)
        check_widget.setLayout(lay_out)
        self.table_widget.setCellWidget(idx, 3, check_widget)
        ckb = self.table_widget.cellWidget(idx, 3).layout().itemAt(0)

        adhoc_item = QTableWidgetItem()
        adhoc_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 4, adhoc_item)

        self.table_widget.setItem(idx, 5, QTableWidgetItem())

        if not student:
            self.write_lock = False

    def open_file(self, index, new=False):
        if self.history_index is not None and self.history_index != len(self.history_files) - 1:
            self.write_file(savefile=True)

        self.current_group_idx = index
        self.history_index = None

        with open(self.name_files[index], 'r', encoding='utf-8') as f:
            students = []
            r = re.compile('\s+✔\s+(\D+)\s(\d+)\s(.*)\s?')
            for line in f:
                m = r.search(line)
                if m:
                    students.append(Student(*(m.group(i) for i in range(1, 4))))

        self.write_lock = True
        self.table_widget.clear()
        labels = 'Name;Matrikelnr.;Gruppe;Anwesend {:02}/{};Adhoc;Kommentar'.format(0, len(students)).split(';')
        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setRowCount(0)
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setHorizontalHeaderLabels(labels)

        for student in students:
            self.add_row(student)

        self.get_savefiles()
        self.history_index = len(self.history_files)
        if self.history_files and not new:
            self.history_undo()
            self.write_lock = False
        else:
            self.write_lock = False
            self.write_file(savefile=True)

        self.update_checkbox_data()
        self.table_widget.resizeColumnsToContents()
        self.table_widget.setSortingEnabled(True)
        self.table_widget.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def update_checkbox_data(self):
        for idx in range(self.table_widget.rowCount()):
            self.table_widget.item(idx, 3).setData(0, int(self.get_checkbox(idx).isChecked()))

    def get_savefiles(self):
        current_group = self.group_combobox.currentText()
        if os.path.exists('Saves'):
            self.history_files = sorted(set(f for f in os.listdir('Saves') if f.startswith(current_group)))

    def history_undo(self):
        if self.history_index:
            self.history_index -= 1
            self.history_load()

    def history_redo(self):
        if self.history_index < len(self.history_files) - 1:
            self.history_index += 1
            self.history_load()

    def history_load(self):
        self.write_lock = True
        self.table_widget.setSortingEnabled(False)
        with open('Saves/' + self.history_files[self.history_index], 'r') as f:
            next(f)
            for line in f:
                matrikelnr, group, attendance, comment = line.strip().split(';')
                adhoc, *comment = comment.split()
                adhoc = adhoc.strip('%')
                if adhoc == '0':
                    adhoc = ''
                comment = ' '.join(comment)

                indices = [idx for idx in range(self.table_widget.rowCount())
                               if self.table_widget.item(idx, 1).text() == matrikelnr]
                if len(indices) == 1:
                    idx = indices[0]
                else:
                    idx = self.table_widget.rowCount()
                    self.add_row()

                self.table_widget.item(idx, 1).setText(matrikelnr)
                self.table_widget.item(idx, 2).setText(group)
                self.get_checkbox(idx).setCheckState(QtCore.Qt.Checked if attendance == 'an' else
                                                     QtCore.Qt.Unchecked)
                self.table_widget.item(idx, 4).setText(adhoc)
                self.table_widget.item(idx, 5).setText(comment)
        self.table_widget.setSortingEnabled(True)
        self.write_lock = False

    def write_file(self, savefile=True):
        if self.write_lock:
            return

        group_name = self.group_combobox.itemText(self.current_group_idx)
        if savefile:
            now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            file_name = 'Saves/{}_{}.csv'.format(group_name, now)
        else:
            file_name = QFileDialog.getSaveFileName(self, 'Export', group_name + '_ueX.csv', 'CSV (*.csv)')[0]
            if not file_name:
                return

        if not os.path.exists('Saves'):
            os.makedirs('Saves')

        with io.open(file_name, 'w', encoding='utf-8', newline='') as f:
            f.write('MatrNr;Gruppe;Kontrolle;Kommentar\n')
            for idx in range(self.table_widget.rowCount()):
                if self.table_widget.item(idx, 1).text():
                    f.write('{};{};{};{}% {}\n'.format(
                        self.table_widget.item(idx, 1).text(),
                        self.table_widget.item(idx, 2).text() or '0',
                        'an' if self.get_checkbox(idx).isChecked() else 'ab',
                        self.table_widget.item(idx, 4).text() or '0',
                        self.table_widget.item(idx, 5).text()
                    ))

        self.history_files.append(file_name[6:])
        self.history_index = len(self.history_files) - 1

    def get_checkbox(self, index):
        return self.table_widget.cellWidget(index, 3).layout().itemAt(0).widget()

    def find_index(self, name):
        indices = [i for i in range(self.table_widget.rowCount())
                   if name.lower() in self.table_widget.item(i, 0).text().lower()]
        return indices[0] if len(indices) == 1 else indices

    def execute_console(self):
        try:
            commands = self.console.text().split(' ')
            name, command = commands[0], ' '.join(commands[1:])
            index = self.find_index(name)
            if isinstance(index, int):
                full_name = self.table_widget.item(index, 0).text()
                if command == 'a':
                    self.get_checkbox(index).setCheckState(QtCore.Qt.Checked)
                    template = '{} ist anwesend'
                elif command == 'b':
                    self.get_checkbox(index).setCheckState(QtCore.Qt.Unchecked)
                    template = '{} ist nicht anwesend'
                elif command.isdigit():
                    self.table_widget.item(index, 4).setText(command)
                    template = '{} erreicht {}%'
                else:
                    self.table_widget.item(index, 5).setText(command)
                    template = '{}: {}'
                self.console_output.setText(template.format(full_name, command))
            else:
                if len(index) == 0:
                    error = 'Der Student "{}" wurde nicht gefunden.'
                else:
                    error = 'Mehrere Studenten treffen auf "{}" zu.'
                self.console_output.setText('Error: ' + error.format(name))

        except IndexError:
            pass

        self.console.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PkToolMainWindow()
    window.show()
    sys.exit(app.exec_())
