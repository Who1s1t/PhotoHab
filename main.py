import sys
from os import listdir
from os.path import isfile, join


import screeninfo
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QGridLayout, QVBoxLayout, \
    QHBoxLayout,  QLabel, QScrollArea, QFrame

from ImageWindow import ImageWindow
from add_folder import AddFolder
from data import db_session
from data.folder import Folder
from filename_has_image_extension import filename_has_image_extension

db_session.global_init("db/SHRD.db")


class FolderSelector(QFrame):
    def __init__(self, set_directory=None):
        QWidget.__init__(self, )

        self.set_directory = set_directory

        self.form = AddFolder(updatet=self.updatet)

        self.layout = QVBoxLayout(self)

        self.add_button = QPushButton("Добавить папку")
        self.add_button.clicked.connect(self.add_folder)

        self.layout.addWidget(self.add_button)

        self.updatet()

    def add_folder(self):
        self.form.show()

    def updatet(self):
        for i in range(1, self.layout.count()):
            self.layout.takeAt(1).widget().deleteLater()

        db_sess = db_session.create_session()
        folders = db_sess.query(Folder).all()
        for folder in folders:
            fold = QLabel(folder.name)
            fold.mousePressEvent = lambda e, path=folder.folder_path: self.set_directory(path)
            self.layout.addWidget(fold)


class ImageFileSelector(QWidget):
    def __init__(self, display_image=None):
        QWidget.__init__(self, )

        self.img_size = 100
        self.album_path = ''
        self.files = ''

        self.display_image = display_image
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setVerticalSpacing(30)
        self.grid_layout.setHorizontalSpacing(30)

    def on_thumbnail_click(self, event, index, img_file_path, all_img, album):

        self.display_image.set_img(img_file_path, album, all_img, index, set_direcory=self.set_directory)
        self.display_image.show()

    def set_directory(self, album_path=''):
        self.album_path = album_path
        if not self.grid_layout.isEmpty():
            row = 0
            col = 0
            for i in range(self.grid_layout.count()):
                l = self.grid_layout.itemAtPosition(row, col).layout()
                l.takeAt(0).widget().deleteLater()
                l.takeAt(0).widget().deleteLater()
                l.deleteLater()
                col += 1
                if col == 5:
                    row += 1
                    col = 0

        files = [f for f in listdir(album_path) if isfile(join(album_path, f))]
        row_in_grid_layout = 0
        column_in_grid_layout = 0

        for i, file_name in enumerate(files):
            if filename_has_image_extension(file_name) is False: continue
            img_label = QLabel()
            text_label = QLabel()
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            file_path = album_path + file_name
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(QSize(self.img_size, self.img_size), Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            img_label.setPixmap(pixmap)
            text_label.setText(file_name)
            img_label.mousePressEvent = \
                lambda e, index=i, file_path=file_path, album=self.album_path, all_img=files: self.on_thumbnail_click(e,
                                                                                                                      index,
                                                                                                                      file_path,
                                                                                                                      all_img,
                                                                                                                      album)
            text_label.mousePressEvent = img_label.mousePressEvent
            thumbnail = QVBoxLayout()
            thumbnail.addWidget(img_label)
            thumbnail.addWidget(text_label)
            self.grid_layout.addLayout(thumbnail, row_in_grid_layout, column_in_grid_layout,
                                       Qt.AlignmentFlag.AlignLeft)

            column_in_grid_layout += 1
            if column_in_grid_layout == 5:
                column_in_grid_layout = 0
                row_in_grid_layout += 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PhotoHub")

        self.main_layout = QGridLayout()

        self.image_file_selector = ImageFileSelector(display_image=ImageWindow())
        self.folder_selector = FolderSelector(set_directory=self.image_file_selector.set_directory)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(screeninfo.get_monitors()[0].width - screeninfo.get_monitors()[0].width // 3)
        scroll.setFixedHeight(screeninfo.get_monitors()[0].height - 440)

        self.but_layout = QHBoxLayout()
        plus_but = QPushButton("+")
        plus_but.clicked.connect(self.size_plus)
        min_but = QPushButton("-")
        min_but.clicked.connect(self.size_min)
        self.but_layout.addWidget(plus_but)
        self.but_layout.addWidget(min_but)

        scroll.setWidget(self.image_file_selector)

        self.main_layout.addWidget(scroll, 0, 1, alignment=Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.folder_selector, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(self.but_layout, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.image_file_selector.set_directory("C:/Users/OVER/PycharmProjects/SHRD/my-album/")

        self.main = QWidget()
        self.main.setLayout(self.main_layout)
        self.setCentralWidget(self.main)

    def size_plus(self):
        self.image_file_selector.img_size += 25
        self.image_file_selector.set_directory(self.image_file_selector.album_path)

    def size_min(self):
        self.image_file_selector.img_size -= 25
        self.image_file_selector.set_directory(self.image_file_selector.album_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    app.exec()
