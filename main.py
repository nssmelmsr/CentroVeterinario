import sys
from PySide6.QtWidgets import * 
from PySide6 import  QtSql, QtWidgets
from PySide6.QtCore import Qt
from mainwindow import Ui_MainWindow
from cajawin import caja_win
from consulwin import ConsWindow
import connectDB
import os, json


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Cargar el archivo .ui
        #uic.loadUi("UI/main.ui", self)
        self.setupUi(self)     
        self.consul_win = ConsWindow(self)
        self.caja_win = caja_win(self)
        #Hacer cosas con los widgets
        self.stackedWidget.setCurrentIndex(0) #muestra pantalla principal
        self.wrong_up_label.hide()
        self.Pass_le.hide()
        self.pass_label.hide()
        self.login_btn.clicked.connect(self.check_login)
        self.exit_btn.clicked.connect(self.close)
        self.exit_btn_2.clicked.connect(self.close)
        self.admin_SE_button.clicked.connect(self.guardar_cambios)

        #self.caja_win.close_connections(
        
        self.send = []                                  ##### lista para el  consultorio 
        
    def check_login(self):
        if (self.Login_combobox.currentText() == 'Consultorio'): #and (self.Pass_le.text() == 'consul123')) :
            self.stackedWidget.setCurrentIndex(2)
            print('conectado como consultorio')
            connectDB.conectarDB()                     ### Database
            self.consul_win


        elif (self.Login_combobox.currentText() == 'Caja'): #and (self.Pass_le.text() == 'caja123')) :
            self.stackedWidget.setCurrentIndex(1)
            print("conectado como caja")
            connectDB.conectarDB()                     ### Database
            self.caja_win
            
        
        elif (self.Login_combobox.currentText == 'Admin'):
            self.Pass_le.show()
            self.pass_label.show()
            if self.Pass_le.text() == 'admin.1204':
                print("conectado como administrador")
                self.stackedWidget.setCurrentIndex(3)
        #else:
            #self.wrong_up_label.show()

    def guardar_cambios(self):
        if os.path.exists(f"myinf"):

            
            with open(f"myinf/info.json", "w") as conffile:
                json.dump({
                    "IP_caja" : self.IP_le.text()},
                    conffile)
                conffile.close()
        else:
                os.mkdir(f"myinf")
                


    def keyPressEvent(self, e):
        if self.stackedWidget.currentIndex() == 0:    ##login
            if e.key() == Qt.Key_Return:
                self.check_login()
        elif self.stackedWidget.currentIndex() == 2:    ##consultorio
            if e.key() == Qt.Key_Delete:
                self.remove_item()

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())