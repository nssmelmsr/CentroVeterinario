import sys
from PySide6.QtWidgets import * 
from PySide6 import  QtSql, QtWidgets
from PySide6.QtCore import Qt
from mainwindow import Ui_MainWindow
#from consulwin import consul_win
import connectDB


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Cargar el archivo .ui
        #uic.loadUi("UI/main.ui", self)
        self.setupUi(self)     

        #Hacer cosas con los widgets
        self.stackedWidget.setCurrentIndex(0) #muestra pantalla principal
        self.wrong_up_label.hide()
        self.Pass_le.setDisabled(True)
        self.login_btn.clicked.connect(self.check_login)
        self.exit_btn.clicked.connect(self.close)
        self.exit_btn_2.clicked.connect(self.close)
        if self.Login_combobox.currentText() == 'Admin':
            self.Pass_le.setEnabled(True)
        
        
    def check_login(self):
        if (self.Login_combobox.currentText() == 'Consultorio'): #and (self.Pass_le.text() == 'consul123')) :
            self.wrong_dr.hide()
            self.stackedWidget.setCurrentIndex(2)
            print('conectado como consultorio')
            connectDB.conectarDB()                     ### Database
            self.busq_consul_le.textChanged.connect(self.consul_search)
            self.consul_comboBox.currentIndexChanged.connect(self.consul_search)

        elif (self.Login_combobox.currentText() == 'Caja'): #and (self.Pass_le.text() == 'caja123')) :
            self.stackedWidget.setCurrentIndex(1)
            print("conectado como caja")
            connectDB.conectarDB()                     ### Database
            self.faltantes()
            self.inv_le.textChanged.connect(self.inventario)
            self.inv_comboBox.currentIndexChanged.connect(self.inventario)
        
        elif ((self.Login_combobox.currentText == 'Admin') and (self.Pass_le.text() == 'admin.1204')):
            print("conectado como administrador")

        else:
            self.wrong_up_label.show()


    def keyPressEvent(self, e):
        if e.key()  == Qt.Key_Return:
            if self.stackedWidget.currentIndex() == 0:
                self.check_login()
    
    

    def faltantes(self):
        self.table_falt.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.table_falt.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table_falt.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.table_falt.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.table_inv.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_inv.setSelectionBehavior(QAbstractItemView.SelectRows)        
        
        self.modelo_falt = QtSql.QSqlQueryModel()
        # Personalizar los encabezados de las columnas
        self.modelo_falt.setHeaderData(0, Qt.Horizontal, "Producto")
        self.modelo_falt.setHeaderData(1, Qt.Horizontal, "Faltantes")
        self.modelo_falt.setHeaderData(2, Qt.Horizontal, "Proveedor")
        self.modelo_falt.setHeaderData(3, Qt.Horizontal, "Teléfono")

        self.modelo_falt.setQuery("select prd.producto, prd.stock_max-prd.stock as faltantes, pv.nombre, pv.tel_contacto from proveedores pv right join productos prd on pv.id = prd.proveedor;")  # Consulta SQL

        if self.table_falt:
            self.table_falt.setModel(self.modelo_falt)
        else:
            print("Error: no se encontró la tabla")
        
        if self.modelo_falt.lastError().isValid():
            print("Error SQL:", self.modelo_falt.lastError().text())

    def inventario(self) : 
       # if self.inv_le.textChanged() or self.inv_comboBox.currentIndexChanged():
            table_select = self.inv_comboBox.currentText()
            search_value = self.inv_le.text()
            
            # Personalizar los encabezados de las columnas

            self.table_inv.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.table_inv.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.table_inv.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.table_inv.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.table_inv.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.table_inv.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

            #self.table_inv.setEditTriggers(QAbstractItemView.NoEd)
            self.table_inv.setSelectionMode(QAbstractItemView.SingleSelection)
            self.table_inv.setSelectionBehavior(QAbstractItemView.SelectRows)

            self.modelo_inv = QtSql.QSqlQueryModel()
            self.modelo_inv.setHeaderData(0, Qt.Horizontal, "Código")
            self.modelo_inv.setHeaderData(1, Qt.Horizontal, "Producto")
            self.modelo_inv.setHeaderData(2, Qt.Horizontal, "Stock")
            self.modelo_inv.setHeaderData(3, Qt.Horizontal, "Stock Mínimo")
            self.modelo_inv.setHeaderData(4, Qt.Horizontal, "Stock Máximo")
            self.modelo_inv.setHeaderData(5, Qt.Horizontal, "Precio")

            if table_select == "productos":
                self.modelo_inv.setQuery("SELECT CB as códido,producto as Producto,stock as Stock,stock_min as Stock mínimo,stock_max as Stock máximo,precio as Precio FROM productos where producto like '%" + search_value + "%' or CB like '%" + search_value + "%';")  # Consulta SQL
            elif table_select == "servicios":
                self.modelo_inv.setQuery("SELECT producto,precio FROM servicios where producto like '%" + search_value + "%';")  # Consulta SQL

            if self.modelo_inv.lastError().isValid():
                print("Error SQL:", self.modelo_inv.lastError().text())

            if self.table_inv:
                self.table_inv.setModel(self.modelo_inv)
            else:
                print("Error: no se encontró la tabla")
    
    def consul_search(self):
        self.wrong_dr.hide()
        table_select_c = self.consul_comboBox.currentText()
        search_value_c = self.busq_consul_le.text()
        
        
        self.busca_cuenta.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.busca_cuenta.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.busca_cuenta.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.busca_cuenta.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.busca_cuenta.setSelectionMode(QAbstractItemView.SingleSelection)
        self.busca_cuenta.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.modelo_consul = QtSql.QSqlQueryModel()
        if table_select_c == "productos":
            self.modelo_consul.setQuery("SELECT CB,producto,stock,stock_min,stock_max,precio FROM productos where producto like '%" + search_value_c + "%' or CB like '%" + search_value_c + "%';")  # Consulta SQL
        elif table_select_c == "servicios":
            self.modelo_consul.setQuery("SELECT producto,precio FROM servicios where producto like '%" + search_value_c + "%';")  # Consulta SQL
        

        #self.busca_cuenta.setHeaderData(0, Qt.Horizontal, "Código")
        #self.busca_cuenta.setHeaderData(1, Qt.Horizontal, "Producto")
        #self.busca_cuenta.setHeaderData(2, Qt.Horizontal, "Stock")
        #self.busca_cuenta.setHeaderData(3, Qt.Horizontal, "Precio")

        if self.modelo_consul.lastError().isValid():
            print("Error SQL:", self.modelo_consul.lastError().text())
        if self.busca_cuenta:
            self.busca_cuenta.setModel(self.modelo_consul)
        else:
            print("Error: no se encontró la tabla")

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())