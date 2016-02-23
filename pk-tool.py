import io
import os
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QCheckBox, QWidget, \
    QHBoxLayout, QInputDialog, QMessageBox
from ui.mainwindow import Ui_MainWindow
from src.group_infos import GroupInfos, Student
from src.settings import Settings
from dialog.settingsdialog import SettingsDialog
from dialog.gitdialog import GitDialog

use_git = True
try:
    from git import Repo, FetchInfo
except ImportError:
    use_git = False


class PkToolMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, use_git):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.group_infos = GroupInfos(repo_path='')
        self.csv_files = dict()
        self.current_data = []
        self.history = []
        self.history_foreward = []
        self.history_lock = False
        self.write_lock = False

        self.table_widget.cellChanged.connect(self.export_csv)
        self.console.returnPressed.connect(self.execute_console)
        self.action_new.triggered.connect(self.new_csv)
        self.action_add_student.triggered.connect(self.new_student)
        self.action_undo.triggered.connect(self.undo_history)
        self.action_redo.triggered.connect(lambda: self.undo_history(True))
        self.action_about.triggered.connect(self.show_about)
        self.action_settings.triggered.connect(self.open_settings)
        self.group_type_combobox.currentIndexChanged.connect(self.fill_group_names_combobox)
        self.group_combobox.currentIndexChanged.connect(self.populate_files)
        self.file_combobox.currentIndexChanged.connect(self.load_group_data)
        self.action_get_email.triggered.connect(self.get_email)
        self.action_commit_and_push.triggered.connect(self.open_git_dialog)

        self.settings = Settings()
        pk_repo_path = self.settings.get_repo_path()
        self.use_git_interactions = use_git
        if not self.settings.get_use_git():
            self.use_git_interactions = False

        self.try_reading_repo()

    def try_git_pull(self):
        pk_repo_path = self.settings.get_repo_path()
        if pk_repo_path and self.use_git_interactions:
            try:
                self.repo = Repo(pk_repo_path)
                o = self.repo.remotes.origin
                info = o.pull()[0]

                if info.flags & (FetchInfo.ERROR | FetchInfo.REJECTED):
                    self.use_git_interactions = False
            except:
                self.use_git_interactions = False
            if not self.use_git_interactions:
                QMessageBox.about(self, 'Fehler', 'Es gab einen Fehler beim Pullen des Git-Repos. \n'
                                  'Git-Interaktionen wurden für diese Session ausgeschaltet.')

        if self.use_git_interactions:
            self.action_commit_and_push.setEnabled(True)
        else:
            self.action_commit_and_push.setDisabled(True)

    def get_changed_or_untracked_files(self):
        self.repo.head.reset(index=True, working_tree=False)
        files = self.repo.untracked_files + [info.a_path for info in self.repo.index.diff(None)]
        return files

    def show_about(self):
        QMessageBox.about(self, 'About', 'https://github.com/jakobkogler/pk-tool')

    def open_settings(self):
        """Opens the settings-dialog, which allows to define the path to the pk-repo and the username
        Updates everything after closing.
        """
        settings_dialog = SettingsDialog(self.settings)
        settings_dialog.exec_()

        self.use_git_interactions = self.settings.get_use_git()
        self.try_reading_repo()

    def try_reading_repo(self):
        self.try_git_pull()
        try:
            self.group_infos = GroupInfos(repo_path=self.settings.get_repo_path())
            self.group_type_combobox.clear()
            self.group_type_combobox.addItems('Meine Alle Normal Fortgeschritten'.split())
            self.fill_group_names_combobox()
            self.populate_files()
            self.load_group_data()

        except:
            pass

    def fill_group_names_combobox(self):
        """Populate the combobox with all the group names,
        that apply for the group type specified in the form.
        """
        type_index = self.group_type_combobox.currentIndex()

        if type_index == 0:
            tutor_name = self.settings.get_username()
            group_names = self.group_infos.get_involved_groups(tutor_name)
        else:
            allowed_types = []
            if type_index == 1:
                allowed_types = ['normal', 'fortgeschritten']
            elif type_index == 2:
                allowed_types = ['normal']
            elif type_index == 3:
                allowed_types = ['fortgeschritten']
            group_names = self.group_infos.get_group_names(allowed_types=allowed_types)

        self.group_combobox.clear()
        group_names.sort(key=lambda name: ('mo di mi do fr'.split().index(name[:2]),name[2:]))
        self.group_combobox.addItems(group_names)

    def new_student(self):
        self.write_lock = True
        self.table_widget.setSortingEnabled(False)
        matrikelnr, ok = QInputDialog.getText(self, 'Neuen Studenten hinzufügen', 'Matrikelnummer:')
        if ok and matrikelnr:
            student = self.get_student(matrikelnr)
            if student:
                self.add_row_to_table(student)
                text = '{} hinzugefügt'.format(student.name)
                self.add_new_history((matrikelnr, text, 1, None, student))
        self.table_widget.setSortingEnabled(True)
        self.write_lock = False


    def load_group_data(self):
        """Load all data for a specific group.
        It updates the names of the instructor and tutors and loads the last available csv-file for this group.
        """
        group_name = self.group_combobox.currentText()
        try:
            info = self.group_infos.get_group_info(group_name)
            self.label_instructor_name.setText(info.instructor)
            self.label_tutor1_name.setText(info.tutor1)
            self.label_tutor2_name.setText(info.tutor2)
        except KeyError:
            pass

        self.write_lock = True
        self.history = []
        self.history_foreward = []
        self.table_widget.clear()
        self.table_widget.setRowCount(0)

        if not self.file_combobox.currentText() or not group_name:
            self.table_widget.setColumnCount(0)
            return

        labels = 'Name;Matrikelnr.;Gruppe;Anwesend 00/00;Adhoc;Kommentar'.split(';')
        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setHorizontalHeaderLabels(labels)

        group = self.group_infos.get_group_info(group_name)
        for student in group.students:
            self.add_row_to_table(student)

        self.load_csv_file(self.get_csv_path())

        self.table_widget.resizeColumnsToContents()
        self.table_widget.setSortingEnabled(True)
        self.table_widget.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.write_lock = False
        self.current_data = self.get_data()
        self.show_last_history()

    def get_email(self):
        clipboard = QApplication.clipboard()
        group_name = self.group_combobox.currentText()
        group = self.group_infos.get_group_info(group_name)
        emails = [student.email for student in group.students]
        clipboard.setText(', '.join(emails))

    def add_row_to_table(self, student):
        """Adds a new row to the table and fills this row with the student's data
        """
        idx = self.table_widget.rowCount()
        self.table_widget.setRowCount(idx + 1)

        name_item = QTableWidgetItem(student.name)
        name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.table_widget.setItem(idx, 0, name_item)

        matrikelnr_item = QTableWidgetItem(student.matrikelnr)
        matrikelnr_item.setFlags(matrikelnr_item.flags() & ~QtCore.Qt.ItemIsEditable)
        matrikelnr_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 1, matrikelnr_item)

        group_item = QTableWidgetItem(student.group_name)
        group_item.setFlags(matrikelnr_item.flags() & ~QtCore.Qt.ItemIsEditable)
        group_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 2, group_item)

        check_item = QTableWidgetItem()
        check_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table_widget.setItem(idx, 3, check_item)
        check_widget = QWidget()
        chk_bx = QCheckBox()
        chk_bx.setCheckState(QtCore.Qt.Unchecked)
        chk_bx.stateChanged.connect(self.attendance_changed)
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

    def get_csv_path(self):
        """Returns the path to the csv-file
        """
        return self.csv_files[self.file_combobox.currentText()]

    def new_csv(self):
        path_suggestion = '/Anwesenheiten/Uebungen/' + self.group_combobox.currentText() + '_ue' + str(len(self.file_combobox) + 1) + '.csv'

        directory = self.settings.get_repo_path()
        path = QFileDialog.getSaveFileName(self, 'Neue CSV-Datei', directory + path_suggestion, '*.csv')[0]
        if not path:
            return

        if not path.endswith('.csv'):
            path += '.csv'

        with io.open(path, 'w', encoding='utf-8', newline='') as f:
            f.write('MatrNr;Gruppe;Kontrolle;Kommentar\n')

        self.populate_files()
        index = self.file_combobox.count() - 1
        for i in range(self.file_combobox.count()):
            if path.endswith(self.file_combobox.itemText(i)):
                index = i
        self.file_combobox.setCurrentIndex(index)

    def populate_files(self):
        """Finds the csv files for this group and populates the combobox
        """
        group_name = self.group_combobox.currentText()
        path = self.settings.get_repo_path() + '/Anwesenheiten/Uebungen/'
        self.csv_files = {os.path.join(os.path.basename(root), name): os.path.join(root, name)
                 for root, dirs, files in os.walk(path)
                 for name in files
                 if name.startswith(group_name)}

        self.file_combobox.clear()
        self.file_combobox.addItems(sorted(self.csv_files.keys()))
        self.file_combobox.setCurrentIndex(self.file_combobox.count() - 1)


    def load_csv_file(self, path):
        """Load a lesson-csv-file and update the table with it's data
        """
        with open(path, 'r', encoding='utf-8') as f:
            next(f)
            for line in f:
                matrikelnr, group_name, attendance, comment = line.strip().split(';')
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
                    new_student = self.get_student(matrikelnr)
                    if new_student:
                        self.add_row_to_table(new_student)
                    else:
                        self.add_row_to_table(Student('', matrikelnr, '', group_name))

                self.table_widget.item(idx, 1).setText(matrikelnr)
                self.table_widget.item(idx, 2).setText(group_name)
                self.get_checkbox(idx).setCheckState(QtCore.Qt.Checked if attendance == 'an' else
                                                     QtCore.Qt.Unchecked)
                self.table_widget.item(idx, 4).setText(adhoc)
                self.table_widget.item(idx, 5).setText(comment)

    def get_student(self, matrikelnr):
        """Finds the student object for a given matrikelnr
        """
        for group_name in self.group_infos.get_group_names():
            group = self.group_infos.get_group_info(group_name)
            for student in group.students:
                if student.matrikelnr == matrikelnr:
                    return student
        else:
            return Student('', matrikelnr, '', self.group_combobox.currentText())

    def get_checkbox(self, index):
        """Returns the checkbox for a specific index
        """
        return self.table_widget.cellWidget(index, 3).layout().itemAt(0).widget()

    def attendance_changed(self):
        """Update the attendance-statistic
        """
        self.export_csv()
        count = sum(self.get_checkbox(index).isChecked() for index in range(self.table_widget.rowCount()))
        attendance = 'Anwesend {}/{}'.format(count, self.table_widget.rowCount())
        self.table_widget.setHorizontalHeaderItem(3, QTableWidgetItem(attendance))

    def export_csv(self):
        """Write the opened table to a csv-file
        """
        if self.write_lock:
            return

        if not self.history_lock:
            self.get_changes()

        path = self.get_csv_path()

        order = dict()
        with open(path, 'r', encoding='utf-8') as f:
            next(f)
            for idx, line in enumerate(f):
                matrikelnr = line.split(';')[0]
                order[matrikelnr] = idx

        with io.open(path, 'w', encoding='utf-8', newline='') as f:
            f.write('MatrNr;Gruppe;Kontrolle;Kommentar\n')
            data = self.get_data()
            data.sort(key=lambda t: order.get(t[0], 999))
            for d in data:
                f.write('{};{};{};{}% {}\n'.format(*d))

        self.show_last_history()

    def get_changes(self):
        data = self.get_data()
        if len(data) == len(self.current_data):
            for new, current in zip(data, self.current_data):
                if new != current:
                    student = self.get_student(new[0])
                    student_name = student.name if student.name else student.matrikelnr
                    if new[2] == 'an' != current[2]:
                        text = '{} ist anwesend'.format(student_name)
                        self.add_new_history((new[0], text, 2, 'ab', 'an'))
                    if new[2] == 'ab' != current[2]:
                        text = '{} ist nicht anwesend'.format(student_name)
                        self.add_new_history((new[0], text, 2, 'an', 'ab'))
                    if new[3] != current[3]:
                        text = '{} erreicht {} bei der Adhoc-Aufgabe'.format(student_name, new[3])
                        self.add_new_history((new[0], text, 3, current[3], new[3]))
                    if new[4] != current[4]:
                        text = '{}: {}'.format(student_name, new[4])
                        self.add_new_history((new[0], text, 4, current[4], new[4]))

        self.current_data = data

    def add_new_history(self, history):
        self.history.append(history)
        self.history_foreward = []
        self.write_console(history[1])
        self.show_last_history()

    def undo_history(self, reverse=False):
        self.history_lock = True
        last_history = None
        if not reverse:
            if len(self.history):
                last_history = self.history.pop()
                new_history = (last_history[0], last_history[1], last_history[2], last_history[4], last_history[3])
                self.history_foreward.append(new_history)
                self.write_console('Rückgängig: {}'.format(last_history[1]))
        else:
            if len(self.history_foreward):
                last_history = self.history_foreward.pop()
                new_history = (last_history[0], last_history[1], last_history[2], last_history[4], last_history[3])
                self.history.append(new_history)
                self.write_console('Wiederherstellen: {}'.format(last_history[1]))

        if last_history is None:
            return

        self.table_widget.setSortingEnabled(False)

        index = -1
        for i in range(self.table_widget.rowCount()):
            if self.table_widget.item(i, 1).text() == last_history[0]:
                index = i
                break
        if index >= 0:
            if last_history[2] == 1:
                if not last_history[3]:
                    self.table_widget.removeRow(index)
                else:
                    self.add_row_to_table(last_history[3])
            if last_history[2] == 2:
                self.get_checkbox(index).setCheckState(QtCore.Qt.Checked if last_history[3] == 'an' else
                                                       QtCore.Qt.Unchecked)
            if last_history[2] in [3, 4]:
                self.table_widget.item(index, last_history[2] + 1).setText(last_history[3])

        self.table_widget.setSortingEnabled(True)
        self.current_data = self.get_data()

        self.show_last_history()
        self.history_lock = False

    def show_last_history(self):
        if self.history:
            message = self.history[-1][1]
            self.action_undo.setEnabled(True)
            self.action_undo.setText('Zurück ({})'.format(message))
        else:
            self.action_undo.setText('Zurück')
            self.action_undo.setEnabled(False)

        if self.history_foreward:
            message = self.history_foreward[-1][1]
            self.action_redo.setEnabled(True)
            self.action_redo.setText('Vor ({})'.format(message))
        else:
            self.action_redo.setText('Vor')
            self.action_redo.setEnabled(False)

    def get_data(self):
        data = []
        for idx in range(self.table_widget.rowCount()):
            if self.table_widget.item(idx, 1).text():
                data.append((
                    self.table_widget.item(idx, 1).text(),
                    self.table_widget.item(idx, 2).text() or '0',
                    'an' if self.get_checkbox(idx).isChecked() else 'ab',
                    self.table_widget.item(idx, 4).text() or '0',
                    self.table_widget.item(idx, 5).text()
                ))
        return sorted(data)

    def find_index(self, identification):
        """Find the index of a student in the table
        """
        indices = [i for i in range(self.table_widget.rowCount())
                   if identification.lower() in self.table_widget.item(i, 0).text().lower() or
                   identification == self.table_widget.item(i, 1).text()]
        return indices[0] if len(indices) == 1 else indices

    def execute_console(self):
        """Executes a command from the console
        'name a' checks the attendance
        'name b' unchecks the attendance
        'name number' writes the adhoc-points
        'name other' writes a comment
        """
        try:
            commands = self.console.text().split(' ')
            identification, command = commands[0], ' '.join(commands[1:])
            index = self.find_index(identification)
            if isinstance(index, int):
                if command == 'a':
                    self.get_checkbox(index).setCheckState(QtCore.Qt.Checked)
                elif command == 'b':
                    self.get_checkbox(index).setCheckState(QtCore.Qt.Unchecked)
                elif command.isdigit():
                    self.table_widget.item(index, 4).setText(command)
                else:
                    self.table_widget.item(index, 5).setText(command)
            else:
                if len(index) == 0:
                    error = 'Der Student "{}" wurde nicht gefunden.'
                else:
                    error = 'Mehrere Studenten treffen auf "{}" zu.'
                self.write_console('Error: ' + error.format(identification))
        except IndexError:
            pass

        self.console.clear()

    def write_console(self, text):
        self.console_output.setText(text)

    def open_git_dialog(self):
        if self.use_git_interactions:
            git_dialog = GitDialog(self.repo, self.get_changed_or_untracked_files())
            git_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PkToolMainWindow(use_git)
    window.show()
    sys.exit(app.exec_())
