#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMainWindow, QGridLayout, QFileDialog, QLabel
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QImage
from skimage.io import imread
from Neural1 import start_detect
from Neural1 import start_training

#
class Example(QWidget):

    def __init__(self):
        super().__init__()

        self._grid = None
        self.initUI()
        self._network = None
        self.flag = False
        self.result_text = None


    def initUI(self):

# Создаётся экземпляр QGridLayout,
# устанавливаем промежуток,
# QGridLayout назначается как макет окна приложения.
        self._grid = QGridLayout(self)
        self._grid.setSpacing(10)
        self.setLayout(self._grid)



# Мы создаем кнопку. Кнопка является экземпляром класса QPushButton.
# Первый параметр конструктора - название кнопки. Вторым параметром является родительский виджет.
# Родительский виджет является виджетом Example.
        button_start_train = QPushButton('Start training', self)
        button_start_train.clicked.connect(self.button_start_train_clicked)

        button_open_im = QPushButton('Open', self)
        button_open_im.clicked.connect(self.button_open_im_clicked)

        button_exit = QPushButton('Quit', self)
        button_exit.clicked.connect(QCoreApplication.instance().quit)
        button_exit.resize(button_exit.sizeHint())

        self._grid.addWidget(button_start_train, 0, 0)
        self._grid.addWidget(button_open_im, 0, 1)
        self._grid.addWidget(button_exit, 0, 2)

        self.setGeometry(300, 100, 800, 600)
        self.setWindowTitle('Neural')
        self.show()

    def button_start_train_clicked(self):
        self._network = start_training()


    def button_open_im_clicked(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', 'home/nyam/Документы/Neural/')[0]
        image = imread(filename, as_grey=True)
        self.show_image(image)

        if (self._network != None):
            result = start_detect(self._network, filename)
            self.show_result(result)
        else:
            result = 'Сlick on "Start training" \nto learn the neural network'
            self.show_result(result)
            self.flag = True


    def show_image(self, image):
        image_qt = QtGui.QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8)
        pixmap = QPixmap(image_qt)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        self._grid.addWidget(lbl, 1, 1, -1, -1)

    def show_result(self, result):
        if (self.result_text != None):
            self._grid.removeWidget(self.result_text)
            self.result_text.deleteLater()
            self.result_text = None
        self.result_text = QLabel(result, self)
        self.result_text.setFont(QtGui.QFont("Times", 18))
        self._grid.addWidget(self.result_text, 1, 2, -1, -1)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())