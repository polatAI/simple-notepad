import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QPushButton, QLabel, QPlainTextEdit, QStatusBar, QToolBar, \
    QVBoxLayout, QAction, QFileDialog, QMessageBox

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence
from PyQt5.QtPrintSupport import QPrintDialog


import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFontDatabase, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction, QPlainTextEdit


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("THT Notepad")
        self.setWindowIcon(QIcon("./icon/tht.ico"))

        self.screen_width, self.screen_height = self.geometry(
        ).width(), self.geometry().height()
        self.resize(self.screen_width * 2, self.screen_height * 2)

        self.filterTypes = 'Text Document (*.txt);; Python (*.py);; Markdown (*.md)'

        self.path = None

        fixedFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedFont.setPointSize(12)

        mainLayout = QVBoxLayout()

        # editor
        self.editor = QPlainTextEdit()
        self.editor.setFont(fixedFont)
        mainLayout.addWidget(self.editor)

        # stautsBar
        self.status_bar = self.statusBar()

        # app container
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        self.init_file_menu()
        self.init_edit_menu()

    def init_file_menu(self):
        file_menu = self.menuBar().addMenu('&File')

        file_toolbar = QToolBar('File')
        file_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(Qt.BottomToolBarArea, file_toolbar)

        open_file_action = self.create_action(
            self, './icon/file_open.ico', 'Open file...', 'Open file', self.file_open)
        open_file_action.setShortcut(QKeySequence.Open)

        save_file_action = self.create_action(
            self, './icon/save_file.ico', 'Save File', 'Save File', self.save_file)
        save_file_action.setShortcut(QKeySequence.Save)

        save_fileAs_action = self.create_action(
            self, './icon/save_as.ico', 'Save File As...', 'Save File As...', self.save_file_as)
        save_fileAs_action.setShortcut(QKeySequence('Ctrl+Shift+S'))

        print_action = self.create_action(
            self, './icon/printer.ico', 'Print File', 'Print file', self.print_file)
        print_action.setShortcut(QKeySequence.Print)

        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)
        file_menu.addAction(save_fileAs_action)
        file_menu.addAction(print_action)

        file_toolbar.addAction(open_file_action)
        file_toolbar.addAction(save_file_action)
        file_toolbar.addAction(save_fileAs_action)
        file_toolbar.addAction(print_action)

    def init_edit_menu(self):
        edit_menu = self.menuBar().addMenu('&Edit')

        edit_toolbar = QToolBar('Edit')
        edit_toolbar.setIconSize(QSize(60, 60))
        self.addToolBar(Qt.BottomToolBarArea, edit_toolbar)

        undo_action = self.create_action(
            self, './icon/undo.ico', 'Undo', 'Undo', self.editor.undo)
        undo_action.setShortcut(QKeySequence.Undo)

        redo_action = self.create_action(
            self, './icon/redo.ico', 'Redo', 'Redo', self.editor.redo)
        redo_action.setShortcut(QKeySequence.Redo)

        clear_action = self.create_action(
            self, './icon/clear.ico', 'Clear', 'Clear', self.clear_content)

        cut_action = self.create_action(
            self, './icon/cut.ico', 'Cut', 'Cut', self.editor.cut)
        copy_action = self.create_action(
            self, './icon/copy.ico', 'Copy', 'Copy', self.editor.copy)
        paste_action = self.create_action(
            self, './icon/paste.ico', 'Paste', 'Paste', self.editor.paste)
        select_all_action = self.create_action(
            self, './icon/select_all.ico', 'Select All', 'Select All', self.editor.selectAll)

        wrap_text_action = self.create_action(
            self, './icon/wrap_text.ico', 'Wrap Text', 'Wrap text', self.toggle_wrap_text)
        wrap_text_action.setShortcut('Ctrl+Shift+W')

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addAction(clear_action)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(select_all_action)
        edit_menu.addSeparator()
        edit_menu.addAction(wrap_text_action)

    def toggle_wrap_text(self):
        self.editor.setLineWrapMode(not self.editor.lineWrapMode())

    def clear_content(self):
        self.editor.setPlainText('')

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            directory='',
            filter=self.filterTypes
        )

        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def save_file(self):
        if self.path:
            text = self.editor.toPlainText()
            try:
                with open(self.path, 'w') as f:
                    f.write(text)
            except Exception as e:
                self.dialog_message(str(e))
        else:
            self.save_file_as()

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save file as...',
            directory='',
            filter=self.filterTypes
        )

        if path:
            self.path = path
            self.save_file()
            self.update_title()

    def print_file(self):
        printDialog = QPrintDialog()
        if printDialog.exec__():
            self.editor.print_(printDialog.printer())

    def update_title(self):
        self.setWindowTitle(
            '{0} - THT Notepad'.format(os.path.basename(self.path) if self.path else 'Untitled'))

    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def create_action(self, parent, icon_path, action_name, set_status_tip, triggered_method):
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.triggered.connect(triggered_method)
        return action


app = QApplication(sys.argv)
notepad = AppDemo()
notepad.show()
sys.exit(app.exec_())
