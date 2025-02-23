import sys
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QStackedWidget, QPushButton, QLabel, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar el archivo .ui
        uic.loadUi("UI/main.ui", self)
        
        # Acceder a los Widgets 
        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.boton_login = self.findChild(QPushButton, "login_btn")
        self.boton_exit = self.findChild(QPushButton, "exit_btn")
        self.label_wrong = self.findChild(QLabel,"wrong_up_label") 
        self.main_logo = self.findChild(QLabel,"logo_label")


        #Hacer cosas con los widgets
        self.stackedWidget.setCurrentIndex(0)
        self.boton_login.clicked.connect(self.check_login)
        self.label_wrong.hide()
        self.boton_exit.clicked.connect(self.close)
        
        
    def check_login(self):
        self.User_check = self.findChild(QLineEdit, "User_le").text()
        self.Pass_check = self.findChild(QLineEdit, "Pass_le").text()
   
        Pass_check = self.Pass_le.text()
        if ((self.User_check == 'consul1') and (self,Pass_check == 'consul123')) :
            self.stackedWidget.setCurrentIndex(2)
        elif ((self.User_check == 'consul2') and (self,Pass_check == 'consul123')) :
            self.stackedWidget.setCurrentIndex(2)
        elif ((self.User_check == 'caja') and (self,Pass_check == 'caja123')) :
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.label_wrong.show()

    def keyPressEvent(self, e):
        if e.key()  == Qt.Key_Return:
            self.check_login()
    
    def show_consul(self):
         self.boton_exit = self.findChild(QPushButton, "exit_btn_2")
         self.boton_exit.clicked.connect(self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())