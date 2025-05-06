import sys
from PySide6.QtWidgets import * 
from PySide6 import  QtSql
from PySide6.QtCore import Qt
from mainwindow import Ui_MainWindow
#import MySQLdb

from consulwin import consul_win
import connectDB
#import MySQLdb as sql



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Cargar el archivo .ui
        #uic.loadUi("UI/main.ui", self)
        self.setupUi(self)     

        #Hacer cosas con los widgets
        self.stackedWidget.setCurrentIndex(0) #muestra pantalla principal
        self.wrong_up_label.hide()
        self.login_btn.clicked.connect(self.check_login)
        self.exit_btn.clicked.connect(self.close)
        
        
    def check_login(self):
        if ((self.User_le == 'consul') and (self.Pass_le == 'consul123')) :
            self.stackedWidget.setCurrentIndex(2)
            consul_win()
        elif ((self.User_le.text() == 'caja') and (self.Pass_le.text() == 'caja123')) :
            self.stackedWidget.setCurrentIndex(1)
            connectDB.conectarDB()
            self.faltantes()
            self.inv_le.textChanged.connect(self.inventario)
            self.inv_comboBox.currentIndexChanged.connect(self.inventario)

        else:
            self.wrong_up_label.show()

    def keyPressEvent(self, e):
        if e.key()  == Qt.Key_Return:
            self.check_login()
    
    def show_consul(self):
         self.exit_btn_2.clicked.connect(self.close)

    def faltantes(self):
        self.modelo_falt = QtSql.QSqlQueryModel()
        self.modelo_falt.setQuery("select prd.producto, prd.stock_max-prd.stock as faltantes, pv.nombre, pv.tel_contacto from proveedores pv right join productos prd on pv.id = prd.proveedor;")  # Consulta SQL
        
        if self.modelo_falt.lastError().isValid():
            print("Error SQL:", self.modelo_falt.lastError().text())
        # Personalizar los encabezados de las columnas
        self.modelo_falt.setHeaderData(0, Qt.Horizontal, "Producto")
        self.modelo_falt.setHeaderData(1, Qt.Horizontal, "Faltantes")
        self.modelo_falt.setHeaderData(2, Qt.Horizontal, "Proveedor")
        self.modelo_falt.setHeaderData(3, Qt.Horizontal, "Teléfono")
        
        if self.table_falt:
            self.table_falt.setModel(self.modelo_falt)
        else:
            print("Error: no se encontró la tabla")
        #self.table_falt.setModel(self.modelo)
    def inventario(self):
        
       # if self.inv_le.textChanged() or self.inv_comboBox.currentIndexChanged():
            self.modelo_inv = QtSql.QSqlQueryModel()
            table_select = self.inv_comboBox.currentText()
            search_value = self.inv_le.text()
            self.modelo_inv.setQuery("SELECT CB,producto,stock,precio FROM " + table_select + " where producto like '%" + search_value + "%' or CB like '%" + search_value + "%';")  # Consulta SQL

            if self.modelo_inv.lastError().isValid():
                print("Error SQL:", self.modelo_inv.lastError().text())
            
            # Personalizar los encabezados de las columnas
            #self.modelo_inv.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            self.modelo_inv.setHeaderData(0, Qt.Horizontal, "Código")
            self.modelo_inv.setHeaderData(1, Qt.Horizontal, "Producto")
            self.modelo_inv.setHeaderData(2, Qt.Horizontal, "Stock")
            self.modelo_inv.setHeaderData(3, Qt.Horizontal, "Precio")
        
            if self.table_inv:
                self.table_inv.setModel(self.modelo_inv)
            else:
                print("Error: no se encontró la tabla")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())