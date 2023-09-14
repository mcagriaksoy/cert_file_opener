__author__ = 'Mehmet Cagri Aksoy - github.com/mcagriaksoy'

from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt6.uic import loadUi
import sys, subprocess

class main_window(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('main_window.ui', self)
        self.pushButton.clicked.connect(self.openCertFile)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.clicked.connect(self.mainProcess)
        self.pushButton_3.clicked.connect(self.clearText)

    def openCertFile(self):
        global fileName
        fileName = QFileDialog.getOpenFileName(self, 'Open cert file:', "", '*.pem | *.crt | *.cer | *.der | *.p7b | *.p7c | *.p12 | *.pfx')
        if fileName:
            self.textEdit.setText(fileName[0])
            self.pushButton_2.setEnabled(True)
        
        return fileName[0]

    def clearText(self):
        self.textEdit_2.setText("")

    def checkRadioButton(self):
        if self.radioButton.isChecked():
            return 'psa'
        elif self.radioButton_2.isChecked():
            return 'x509'
        elif self.radioButton_3.isChecked():
            return 'ec'
        else:
            self.textEdit_2.setText("Please select a certificate type!!!")
            return False

    # call openssl command
    def decryptCertificate(self):
        buttonSelection = self.checkRadioButton()
        if not buttonSelection:
            self.pushButton_2.setEnabled(False)
            return False

        process = subprocess.Popen(
        ["openssl", buttonSelection, "-in", fileName[0], "-text", "-noout"],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell=True
        )
        self.textEdit_2.setText(process.stdout.read().decode('utf-8'))
        #self.textEdit_2.setText(process.stderr.read().decode('utf-8'))

    def mainProcess(self):   
        self.decryptCertificate()

def start_ui_design():
    app = QApplication(sys.argv)
    widget = main_window()
    widget.show()
    sys.exit(app.exec())
