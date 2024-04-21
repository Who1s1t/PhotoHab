from PyQt6.QtWidgets import QWidget, QFileDialog, QPushButton, QVBoxLayout, QLineEdit

from data import db_session
from data.folder import Folder


class AddFolder(QWidget):
    def __init__(self, updatet=None):
        QWidget.__init__(self, )
        self.updatet = updatet

        self.layout = QVBoxLayout(self)

        self.path = ''
        folder_button = QPushButton("Выбрать папку")
        folder_button.clicked.connect(self.set_folder)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_folder)

        self.name = QLineEdit()

        self.layout.addWidget(folder_button)
        self.layout.addWidget(self.name)
        self.layout.addWidget(add_button)

    def set_folder(self):
        fname = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        print(fname + "/")
        self.path = fname + "/"
        if not fname:
            return

    def add_folder(self):
        if not self.name or not self.path:
            return
        db_sess = db_session.create_session()
        folder = Folder()
        folder.name = self.name.text()
        folder.folder_path = self.path
        db_sess.add(folder)
        db_sess.commit()
        self.updatet()
        self.close()
