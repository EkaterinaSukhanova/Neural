
import sys

from PyQt5 import QtCore

from PyQt5 import QtGui


class Window():
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # initializes the user interface
        self.setupUi(self)

        # restarts the 'QProgressBar' . перезапускает «QProgressBar»
        self.qprogressbar.reset()

        # connects the 'QPushButton.valueChanged()' signal with the 'qprogressbar_value_changed()' slot. подключает сигнал «QPushButton.valueChanged ()» с слотом «qprogressbar_value_changed ()»
        self.qprogressbar.valueChanged.connect(self.qprogressbar_value_changed)

        # connects the 'QPushButton.clicked()' signal with the 'btn_start_clicked()' slot . подключает сигнал «QPushButton.clicked ()» с слотом «btn_start_clicked ()»
        self.btn_start.clicked.connect(self.btn_start_clicked)

        # sets the icon of 'btn_clear'
        self.btn_clear.setIcon(QtGui.QIcon('images_test/circle1.png'))

        # connects the 'QToolButton.clicked()' signal with the 'clear_output()' slot . подключает сигнал «QToolButton.clicked ()» с слотом «clear_output ()»
        self.btn_clear.clicked.connect(self.btn_clear_output)

        # creates a 'QTimer'
        self.qtimer = QtCore.QTimer()

        # connects the 'QTimer.timeout()' signal with the 'run_progress()' slot
        self.qtimer.timeout.connect(self.qtimer_timeout)

    # 'qtimer_timeout()' slot
    def qtimer_timeout(self):
        # gets the current value of the 'QProgressBar'
        current_value = self.qprogressbar.value()

        # adds 1 to the current value of the 'QProgressBar'
        # 'QProgressBar.setValue()' emits the 'QProgressBar.valueChanged()' signal
        self.qprogressbar.setValue(current_value + 1)

    # 'btn_start_clicked()' slot
    def btn_start_clicked(self):
        # restarts the 'QProgressBar'
        self.qprogressbar.reset()

        # starts the 'QTimer' with an interval of 40 milliseconds
        self.qtimer.start(40)

    # 'btn_clear_output()' slot
    def btn_clear_output(self):
        # clears the content of the 'QPlainTextEdit'
        self.edt_output.clear()

    # 'qprogressbar_value_changed()' slot
    def qprogressbar_value_changed(self, value):
        # adds the emitted signal to the 'QPlainTextEdit'
        self.edt_output.appendPlainText(u'valueChanged (value: {})'.format(value))

        # shows the last output text in the 'QPlainTextEdit'
        self.last_output()

        # if 'value' is equal to the maximum value of the 'QProgressBar'
        if value == self.qprogressbar.maximum():
            # stops the 'QTimer'
            self.qtimer.stop()

            # changes the text of 'btn_start'
            self.btn_start.setText(u'&Start')

    def last_output(self):
        """
        Shows the last output text of the 'QPlainTextEdit'.
        """

        self.edt_output.moveCursor(QtGui.QTextCursor.End)


# creates the application
application = QtGui.QApplication(sys.argv)

# creates the window
window = Window()

# shows the window
window.show()

# runs the application
sys.exit(application.exec_())