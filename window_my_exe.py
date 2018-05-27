#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt5 import QtCore, QtGui
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMainWindow, QGridLayout, QFileDialog, QLabel, QProgressBar
from PyQt5.QtCore import QCoreApplication, QBasicTimer
from PyQt5.QtGui import QPixmap, QImage
from skimage.io import imread
from Neural1 import start_detect
from Neural1 import start_training
import numpy as np
from time import sleep


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
        self.num_epochs = 4000

        # self.progressBar = None

        self.flag_start_show_process = False

    def initUI(self):

# Создаётся экземпляр QGridLayout,
# устанавливаем промежуток,
# QGridLayout назначается как макет окна приложения.
        self._grid = QGridLayout(self)
        # self._grid.setSpacing(10)
        # self._grid.setColumnMinimumWidth(1, 100)
        # self._grid.setRowStretch(1, 50)

        self.setLayout(self._grid)

        self.timer = QBasicTimer()

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

        # self.progressBar = QProgressBar(self)
        # self.progressBar.resize(80, 20)
        # self.progressBar.setGeometry(10, 20, 20, 25)
        # self.progressBar.setRange(0, 1)
        # self._grid.addWidget(self.progressBar, 1, 0, 1, 1)
        #
        # self.start_process_training = TaskThread()
        # self.start_process_training.taskFinished.connect(self.onFinished)

        self.setGeometry(300, 100, 800, 600)
        self.setWindowTitle('Neural')
        self.show()

    def button_start_train_clicked(self):
        # self.progressBar.setRange(0, 0)
        # self.start_process_training()

        label = self.show_MSE_progress_2()

        self._network, self.MSE_progress = start_training(label, QApplication.processEvents)


    # def start_process_training(self):
    #     self._network, self.MSE_progress = start_training()
    #
    # def onFinished(self):
    #     # Stop the pulsation
    #     self.progressBar.setRange(0, 1)
    #     self.progressBar.setValue(1)

    def show_MSE_progress_2(self) -> QLabel:
        self.string_process = QLabel("string", self)
        self.string_process.setFont(QtGui.QFont("Times", 10))
        self._grid.addWidget(self.string_process, 2, 1)
        return self.string_process


    # # self.show_MSE_progress()
    #
    # def show_MSE_progress(self):
    #     self.flag_start_show_process = True
    #     while self.flag_start_show_process == True:
    #         for i in range(self.num_epochs):  # i = 0...3999
    #             QApplication.processEvents()
    #             train_loss = self.MSE_progress[i]
    #             string_on_screen = "\rProgress: {}, Training loss: {}".format(str(100 * i / float(self.num_epochs))[:4], str(train_loss)[:5])
    #             if (self.string_process != None):
    #                 self._grid.removeWidget(self.string_process)
    #                 self.string_process.deleteLater()
    #                 self.string_process = None
    #             self.string_process = QLabel(string_on_screen, self)
    #             self.string_process.setFont(QtGui.QFont("Times", 10))
    #             self._grid.addWidget(self.string_process, 1, 1, -1, -1)
    #     self.flag_start_show_process = False

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

    def show_image(self, image):
        if (self.image_on_screen != None):
            self._grid.removeWidget(self.image_on_screen)
            self.image_on_screen.deleteLater()
            self.image_on_screen = None
        big_image = self.image_resize(image, 5, 5)
        image_qt = QtGui.QImage(big_image.data, big_image.shape[1], big_image.shape[0], QImage.Format_Grayscale8)
        pixmap = QPixmap(image_qt)
        self.image_on_screen = QLabel(self)
        self.image_on_screen.setPixmap(pixmap)
        self._grid.addWidget(self.image_on_screen, 1, 1, -1, -1)

    def image_resize(self, image, k_h: int, k_v: int):
        M = image.shape[0] * k_v
        N = image.shape[1] * k_h
        s = (M, N)
        # s1= (image.shape[0],image.shape[1])
        big_image = np.zeros(s, dtype=np.uint8)
        for i in range(0, image.shape[0]):
            for l in range(0, k_v):
                for j in range(0, image.shape[1]):
                    for k in range(0, k_h):
                        index_i = k_h * i + l
                        index_j = k_v * j + k
                        big_image[index_i][index_j] = image[i][j]
        return big_image

    def show_result(self, result):
        if (self.result_text != None):
            self._grid.removeWidget(self.result_text)
            self.result_text.deleteLater()
            self.result_text = None
        self.result_text = QLabel(result, self)
        self.result_text.setFont(QtGui.QFont("Times", 18))
        self._grid.addWidget(self.result_text, 1, 2, -1, -1)


# class TaskThread(QtCore.QThread):
#     notifyProgress = QtCore.pyqtSignal(int)
#
#     def run(self):
#         for i in range(101):
#             self.notifyProgress.emit(i)
#             self.timer.sleep(0.1)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())