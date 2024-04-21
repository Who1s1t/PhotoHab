import os
from pathlib import Path
import tempfile
import shutil

from PIL import ImageFilter, Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction, QIcon
from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, QGridLayout, QVBoxLayout, QLineEdit, \
    QLabel, QFileDialog

tmpdir = Path(tempfile.mkdtemp())
print(tmpdir)


class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        saveFile = QAction(QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+N')
        saveFile.setStatusTip('Save new File')
        saveFile.triggered.connect(self.save)

        delFile = QAction(QIcon('del.png'), 'Delete', self)
        delFile.setShortcut('Ctrl+D')
        delFile.setStatusTip('Delete file')
        delFile.triggered.connect(self.delete)

        fileMenu.addAction(saveFile)
        fileMenu.addAction(delFile)

        self.set_directory = ''

        blurlabel = QLabel("Размытие")
        blurButton = QPushButton("Применить")
        blurButton.clicked.connect(self.blur)
        self.blurlinr = QLineEdit()

        medflabel = QLabel("Фильтр режима изображения")
        medfButton = QPushButton("Применить")
        medfButton.clicked.connect(self.medf)
        self.medfline = QLineEdit()

        rezButton = QPushButton("Улучшить резкость")
        rezButton.clicked.connect(self.rez)

        detButton = QPushButton("Улучшить детализацию")
        detButton.clicked.connect(self.det)

        rot_button = QPushButton("Повернуть на 90 градусов")
        rot_button.clicked.connect(self.rotate)

        mirror_button = QPushButton("Отразить по горизонтале")
        mirror_button.clicked.connect(self.mirror)

        mirror_top_button = QPushButton("Отразить по вертикале")
        mirror_top_button.clicked.connect(self.mirror_top)

        self.editlayout = QVBoxLayout()
        self.editlayout.addWidget(blurlabel)
        self.editlayout.addWidget(self.blurlinr)
        self.editlayout.addWidget(blurButton)
        self.editlayout.addWidget(medflabel)
        self.editlayout.addWidget(self.medfline)
        self.editlayout.addWidget(medfButton)
        self.editlayout.addWidget(rezButton)
        self.editlayout.addWidget(detButton)
        self.editlayout.addWidget(rot_button)
        self.editlayout.addWidget(mirror_button)
        self.editlayout.addWidget(mirror_top_button)

        self.img_path = ''
        self.orig_path = ''
        self.album = ''
        self.all_img = []
        self.index = 0
        self.img = QPixmap('')

        self.label = QLabel(self)
        self.label.setPixmap(self.img)

        centlour = QVBoxLayout()
        centlour.addWidget(self.label)

        butnext = QPushButton("Дальше")
        butnext.clicked.connect(self.next_but)

        butprev = QPushButton("Назад")
        butprev.clicked.connect(self.prev_but)

        edit_but = QPushButton("Редактировать")
        edit_but.clicked.connect(self.show_edit)

        mainlouut = QGridLayout()

        mainlouut.addWidget(edit_but, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        mainlouut.addWidget(butprev, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        mainlouut.addLayout(centlour, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        mainlouut.addWidget(butnext, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.edit_widget = QWidget()
        self.edit_widget.setWindowTitle("Редактирование")
        self.edit_widget.setLayout(self.editlayout)

        self.setWindowTitle("PhotoHub")
        main = QWidget()
        main.setLayout(mainlouut)

        self.setCentralWidget(main)

    def show_edit(self):
        self.edit_widget.close()
        self.edit_widget.show()

    def blur(self):

        with Image.open(self.img_path) as img_orig:
            img_fil = img_orig.filter(ImageFilter.BoxBlur(int(self.blurlinr.text())))
            img_fil.save(self.img_path)
        self.change()

    def mirror(self):

        with Image.open(self.img_path) as img_orig:
            img_fil = img_orig.transpose(Image.FLIP_LEFT_RIGHT)
            img_fil.save(self.img_path)
        self.change()

    def mirror_top(self):

        with Image.open(self.img_path) as img_orig:
            img_fil = img_orig.transpose(Image.FLIP_TOP_BOTTOM)
            img_fil.save(self.img_path)
        self.change()

    def rotate(self):

        with Image.open(self.img_path) as img_orig:
            img_fil = img_orig.rotate(90, expand=True)
            img_fil.save(self.img_path)
        self.change()

    def rez(self):

        with Image.open(self.img_path) as img_orig:
            img_fil = img_orig.filter(ImageFilter.SHARPEN())
            img_fil.save(self.img_path)
        self.change()

    def det(self):

        with Image.open(self.img_path) as img_orig:
            img_fil = img_orig.filter(ImageFilter.DETAIL())
            img_fil.save(self.img_path)
        self.change()

    def medf(self):

        with Image.open(self.img_path) as img_orig:
            img_fil = img_orig.filter(ImageFilter.ModeFilter(size=int(self.medfline.text())))
            img_fil.save(self.img_path)
        self.change()

    def next_but(self):

        if self.index + 2 > len(self.all_img):
            return
        self.set_img(self.album + self.all_img[self.index + 1], self.album, self.all_img, self.index + 1)

    def prev_but(self):
        if self.index - 1 < 0:
            return
        self.set_img(self.album + self.all_img[self.index - 1], self.album, self.all_img, self.index - 1)

    def save(self):
        if not self.img_path:
            return
        home_dir = str(Path.home())
        fname = QFileDialog.getSaveFileName(self, 'Save', home_dir, f"Images (*{Path(self.img_path).suffix})")
        if not fname[0]:
            return
        shutil.copy2(self.img_path, fname[0])
        print(fname)

    def delete(self):
        os.remove(self.orig_path)
        self.set_directory(self.album)
        self.close()

    def change(self):

        self.img = QPixmap(self.img_path)
        self.label.setPixmap(self.img)

    def set_img(self, file_path, album, all_img, index, set_direcory=None):
        if set_direcory:
            self.set_directory = set_direcory
        self.album = album
        self.all_img = all_img
        self.index = index

        shutil.copy2(file_path, tmpdir / Path(file_path).name)

        self.orig_path = file_path
        self.img_path = str(tmpdir / Path(file_path).name)
        self.change()
