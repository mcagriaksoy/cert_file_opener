__author__ = "Mehmet Cagri Aksoy - github.com/mcagriaksoy"

from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt6.QtGui import QColor
from PyQt6.uic import loadUi
import sys, subprocess

class main_window(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("main_window.ui", self)
        self.pushButton.clicked.connect(self.openCertFile)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.clicked.connect(self.mainProcess)
        self.pushButton_3.clicked.connect(self.clearText)

    def openCertFile(self):
        global fileName
        fileName = QFileDialog.getOpenFileName(self, "Open cert file:", "", "*.pem | *.crt | *.cer | *.der | *.p7b | *.p7c | *.p12 | *.pfx")
        if fileName:
            self.textEdit.setText(fileName[0])
            self.pushButton_2.setEnabled(True)
        
        return fileName[0]

    def clearText(self):
        self.textEdit_2.setText("")

    def checkRadioButton(self):
        if self.radioButton.isChecked():
            return "rsa"
        elif self.radioButton_2.isChecked():
            return "x509"
        elif self.radioButton_3.isChecked():
            return "ec"
        elif self.radioButton_4.isChecked():
            return "pkcs7"
        elif self.radioButton_5.isChecked():
            return "pkcs8"
        elif self.radioButton_6.isChecked():
            return "pkcs12"
        elif self.radioButton_7.isChecked():
            return "pkey"
        elif self.radioButton_8.isChecked():
            return "dsa"
        elif self.radioButton_9.isChecked():
            return "ca"
        else:
            self.textEdit_2.setText("Please select a certificate type!!!")
            return False

    # call openssl command
    def decryptCertificate(self):
        buttonSelection = self.checkRadioButton()
        if not buttonSelection:
            self.pushButton_2.setEnabled(False)
            return False
        
        output = "-noout"
        cmd = ["openssl" , buttonSelection , "-in", fileName[0], "-text" , output]
        if self.checkBox.isChecked():
            output = "-out output.txt"
            cmd = ["openssl" , buttonSelection , "-in", fileName[0], "-text" , output]

        process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text = True
        )

        self.textEdit_2.setText("Please wait...")
        self.textEdit_2.setTextColor(QColor("black"))
        self.textEdit_2.append(process.stdout.read())
        self.textEdit_2.setTextColor(QColor("green"))
        self.textEdit_2.append("Output file created as output.txt")

    def mainProcess(self):   
        self.decryptCertificate()

def start_ui_design():
    app = QApplication(sys.argv)
    widget = main_window()
    widget.show()
    sys.exit(app.exec())
