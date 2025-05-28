from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6 import  QtSql, QtWidgets

class caja_win:
    def __init__(self,main_window):
        #super().__init__()
        self.ui = main_window 
        self.ui.inv_comboBox.currentIndexChanged.connect(self.inventario)
        self.ui.inv_le.textChanged.connect(self.inventario)

    def faltantes(self):
        self.ui.table_falt.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.ui.table_falt.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.ui.table_falt.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.ui.table_falt.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.ui.table_falt.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.table_falt.setSelectionBehavior(QAbstractItemView.SelectRows)        
        
        self.modelo_falt = QtSql.QSqlQueryModel()
        # Personalizar los encabezados de las columnas
        self.modelo_falt.setHeaderData(0, Qt.Horizontal, "Producto")
        self.modelo_falt.setHeaderData(1, Qt.Horizontal, "Faltantes")
        self.modelo_falt.setHeaderData(2, Qt.Horizontal, "Proveedor")
        self.modelo_falt.setHeaderData(3, Qt.Horizontal, "Teléfono")

        if self.ui.table_falt:
            self.ui.table_falt.setModel(self.modelo_falt)
        else:
            print("Error: no se encontró la tabla")
        
        self.modelo_falt.setQuery("select prd.producto, prd.stock_max-prd.stock as faltantes, pv.nombre, pv.tel_contacto from proveedores pv right join productos prd on pv.id = prd.proveedor;")  # Consulta SQL
        
        if self.modelo_falt.lastError().isValid():
            print("Error SQL:", self.modelo_falt.lastError().text())



    def inventario(self) : 
       # if self.inv_le.textChanged() or self.inv_comboBox.currentIndexChanged():
            table_select = self.ui.inv_comboBox.currentText()
            search_value = self.ui.inv_le.text()

            #self.table_inv.setEditTriggers(QAbstractItemView.NoEd)
            self.ui.table_inv.setSelectionMode(QAbstractItemView.SingleSelection)
            self.ui.table_inv.setSelectionBehavior(QAbstractItemView.SelectRows)

            self.modelo_inv = QtSql.QSqlQueryModel()

            if table_select == "productos":
                self.modelo_inv.setQuery("SELECT CB,producto,stock,stock_min ,stock_max,precio FROM productos where producto like '%" + search_value + "%' or CB like '%" + search_value + "%';")  # Consulta SQL
                self.ui.table_inv.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                self.ui.table_inv.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
                self.ui.table_inv.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                self.ui.table_inv.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                self.ui.table_inv.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                self.ui.table_inv.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                # Personalizar los encabezados de las columnas
                self.modelo_inv.setHeaderData(0, Qt.Horizontal, "Código")
                self.modelo_inv.setHeaderData(1, Qt.Horizontal, "Producto")                
                self.modelo_inv.setHeaderData(2, Qt.Horizontal, "Stock")
                self.modelo_inv.setHeaderData(3, Qt.Horizontal, "Stock Mínimo")
                self.modelo_inv.setHeaderData(4, Qt.Horizontal, "Stock Máximo")
                self.modelo_inv.setHeaderData(5, Qt.Horizontal, "Precio")

            elif table_select == "servicios":
                self.modelo_inv.setQuery("SELECT id, producto,precio FROM servicios where producto like '%" + search_value + "%';")  # Consulta SQL
                self.ui.table_inv.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                self.ui.table_inv.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
                self.ui.table_inv.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                self.modelo_inv.setHeaderData(0, Qt.Horizontal, "ID")
                self.modelo_inv.setHeaderData(1, Qt.Horizontal, "Producto")
                self.modelo_inv.setHeaderData(2, Qt.Horizontal, "Precio")                 

            if self.modelo_inv.lastError().isValid():
                print("Error SQL:", self.modelo_inv.lastError().text())

            if self.ui.table_inv:
                self.ui.table_inv.setModel(self.modelo_inv)
            else:
                print("Error: no se encontró la tabla")
