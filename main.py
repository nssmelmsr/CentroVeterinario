import sys
from PySide6.QtWidgets import * 
from PySide6 import  QtSql, QtWidgets
from PySide6.QtCore import Qt
from mainwindow import Ui_MainWindow
from cajawin import caja_win
from consulwin import ConsWindow
import connectDB_orig


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
        self.Pass_le.setDisabled(True)
        self.login_btn.clicked.connect(self.check_login)
        self.exit_btn.clicked.connect(self.close)
        self.exit_btn_2.clicked.connect(self.close)
        #self.caja_win.close_connections()


        self.columnas = ["Code","Item","Precio"]
        self.send = []                                  ##### lista para el  consultorio 
        
    def check_login(self):
        if (self.Login_combobox.currentText() == 'Consultorio'): #and (self.Pass_le.text() == 'consul123')) :
            self.stackedWidget.setCurrentIndex(2)
            print('conectado como consultorio')
            connectDB_orig.conectarDB()                     ### Database
            self.consul_win


        elif (self.Login_combobox.currentText() == 'Caja'): #and (self.Pass_le.text() == 'caja123')) :
            self.stackedWidget.setCurrentIndex(1)
            print("conectado como caja")
            connectDB_orig.conectarDB()                     ### Database
            self.caja_win
            
        
        elif ((self.Login_combobox.currentText == 'Admin') and (self.Pass_le.text() == 'admin.1204')):
            print("conectado como administrador")

        else:
            self.wrong_up_label.show()


    def keyPressEvent(self, e):
        if self.stackedWidget.currentIndex() == 0:    ##login
            if e.key() == Qt.Key_Return:
                self.check_login()
        elif self.stackedWidget.currentIndex() == 2:    ##consultorio
            if e.key() == Qt.Key_Delete:
                self.remove_item

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())