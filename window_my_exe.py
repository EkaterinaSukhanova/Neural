#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt5 import QtCore, QtGui
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QFileDialog, QLabel
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QImage
from skimage.io import imread
from Neural1 import start_detect
from Neural1 import start_training
import numpy as np


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self._grid = None
        self.initUI()

        self._network = None
        self.result_text = None
        self.image_on_screen = None
        self.MSE_progress = None
        self.string_process = None

    def initUI(self):

# Создаётся экземпляр QGridLayout,
# устанавливаем промежуток,
# QGridLayout назначается как макет окна приложения.
        self._grid = QGridLayout(self)
        self.setLayout(self._grid)

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

        self.setGeometry(300, 100, 800, 500)
        self.setWindowTitle('Neural')
        self.show()

    def button_start_train_clicked(self):
        label = self.show_MSE_progress()

        self._network, self.MSE_progress = start_training(label, QApplication.processEvents)

    def show_MSE_progress(self) -> QLabel:
        self.string_process = QLabel("string", self)
        self.string_process.setFont(QtGui.QFont("Times", 18))
        self._grid.addWidget(self.string_process, 1, 0)
        return self.string_process

    def button_open_im_clicked(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', 'home/nyam/Документы/Neural/')[0]
        image = imread(filename, as_grey=True)
        self.show_image(image)

        if (self._network != None):
            result_str, answer_shape = start_detect(self._network, filename)
            self.show_result(result_str, answer_shape)
        else:
            result_str = 'Сlick on "Start training" \nto learn the neural network'
            self.show_result(result_str)

    def show_image(self, image):
        if (self.image_on_screen != None):
            self._grid.removeWidget(self.image_on_screen)
            self.image_on_screen.deleteLater()
            self.image_on_screen = None
        big_image = self.image_resize(image, 7, 7)
        image_qt = QtGui.QImage(big_image.data, big_image.shape[1], big_image.shape[0], QImage.Format_Grayscale8)
        pixmap = QPixmap(image_qt)
        self.image_on_screen = QLabel(self)
        self.image_on_screen.setPixmap(pixmap)
        self._grid.addWidget(self.image_on_screen, 1, 1, -1, -1)

    def image_resize(self, image, k_h: int, k_v: int):
        M = image.shape[0] * k_v
        N = image.shape[1] * k_h
        s = (M, N)
        big_image = np.zeros(s, dtype=np.uint8)
        for i in range(0, image.shape[0]):
            for l in range(0, k_v):
                for j in range(0, image.shape[1]):
                    for k in range(0, k_h):
                        index_i = k_h * i + l
                        index_j = k_v * j + k
                        big_image[index_i][index_j] = image[i][j]
        return big_image

    def show_result(self, result_str, answer_shape = None):
        if (self.result_text != None):
            self._grid.removeWidget(self.result_text)
            self.result_text.deleteLater()
            self.result_text = None
        if answer_shape is not None:
            result_str += "\n"
            result_str += str(answer_shape)
        self.result_text = QLabel(result_str, self)
        self.result_text.setFont(QtGui.QFont("Times", 18))
        self._grid.addWidget(self.result_text, 1, 2, -1, -1)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
