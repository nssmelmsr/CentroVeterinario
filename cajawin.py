from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import *
from PySide6 import QtSql,QtWidgets
from PySide6.QtGui import QStandardItemModel, QStandardItem
from cuentaWidget import Ui_cuenta_view
import socket , datetime, os, json

class muestra_nota(QWidget):
    recibir_prod = Signal(dict)
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.ui = Ui_cuenta_view()
        self.ui.setupUi(self)
        self.columnas = ["Code","Item","Precio"]
        
        self.ui.remove_btn_extra.clicked.connect(self.remove_item)
        self.ui.add_btn_extra.clicked.connect(lambda: self.recibir_prod.emit({}))
        #self.ui.add_btn_extra.clicked.connect(self.recibir_prod.emit)
        self.ui.finish_btn.clicked.connect(self.cuenta_final)

        self.ui.paciente_label_2.setText(datos.get("paciente"))
        self.ui.dr_label.setText(datos.get("medico")) ### cambiar a paciente
        self.ui.Total_label.setText(f"${datos.get('Total', 0):.2f}")
        
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Código", "Servicio", "Precio"])

        for servicio in datos.get("servicios", []):
            row = [
                QStandardItem(str(servicio.get("Code", ""))),
                QStandardItem(servicio.get("Item", "")),
                QStandardItem(f"${servicio.get('Precio', 0):.2f}")
            ]
            self.model.appendRow(row)

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)




    def cuenta_final(self):
        self.close()

    

    def redibujar_tabla(self):      ########################################### tabla de widget
        self.ui.tableView.setRowCount(len(self.model))
        self.ui.tableView.setColumnCount(len(self.columnas))
        self.ui.tableView.setHorizontalHeaderLabels(self.columnas)


        for i, fila in enumerate(self.model):     #fila
            for j, columna in enumerate(self.columnas):     #columna
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, fila[columna]) 
                self.model.setItem(i,j,item)
        
        self.total = sum(item["Precio"] for item in self.model)
        self.ui.label_total.setText(f"Total: ${str(self.total):.2f}")



    def remove_item(self):
        seleccion = self.ui.tableView.selectionModel()
        fila = self.ui.tableView.currentRow()
        if seleccion.hasSelection():
            #self.fila = seleccion.selectedIndexes()[0].row()
            self.model.pop(fila)  # elimina de la lista

            self.redibujar_tabla()

        else:
            print("No hay fila seleccionada para eliminar.")


    def agregar_producto(self,producto:dict):
        row = [
            QStandardItem(str(producto["Code"])),
            QStandardItem(producto["Item"]),
            QStandardItem(f"${producto['Precio']:.2f}")
        ]
        self.model.appendRow(row)

        self.ui.Total_label.setText(f"{self.calcular_Total():.2f}")
        self.redibujar_tabla


    def calcular_Total(self):
        total = 0
        for row in range(self.model.rowCount()):
            precio_item = self.model.item(row, 2).text()
            precio_valor = float(precio_item.replace("$", ""))
            total += precio_valor
        return total
    
'''    def add_cuenta(self):#, seleccion):
        table_select_c = self.ui.inv_comboBox_2.currentText()
        seleccion = self.ui.table_busq.selectionModel()
        if seleccion.hasSelection():
            self.fila = seleccion.selectedIndexes()[0].row()
            if table_select_c  == "productos":
                code_send = self.ui.modelo_caja.index(self.fila,0).data()
                product_send = self.ui.modelo_caja.index(self.fila,1).data()
                price_send = self.ui.modelo_caja.index(self.fila,3).data() 
            elif table_select_c  == "servicios":
                code_send = self.ui.modelo_caja.index(self.fila,0).data()
                product_send = self.ui.modelo_caja.index(self.fila,1).data()
                price_send = self.ui.modelo_caja.index(self.fila,2).data() 

            #print(code_send,product_send,price_send)
            self.model.append({
                "Code" : code_send,
                "Item" : product_send,
                "Precio" : price_send
            })
            self.redibujar_tabla()

        else:
            print("nada seleccionado")
        
        try:
            self.ui.add_btn_extra.clicked.disconnect()        #boton en widget
        except TypeError:
            pass  # No había conexiones previas

'''
        

    

class TCPReceiver(QThread):
    archivo_recibido = Signal(str)  # Emitirá la ruta del archivo recibido

    def __init__(self, host, port, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self.running = True




    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(1)

        while self.running:
            conn, addr = sock.accept()
            print("Conectado con:", addr)

            now = datetime.datetime.now()
            carpeta = now.strftime("%d_%m_%Y")
            filename = "Nota_" + now.strftime("%H%M%S") + ".json"

            os.makedirs(f"cuentas/{carpeta}", exist_ok=True)
            full_path = f"cuentas/{carpeta}/{filename}"

            with open(full_path, "w", encoding="utf-8") as f:
                while True:
                    data = conn.recv(1024).decode("utf-8")
                    if not data:
                        break
                    f.write(data)
            conn.close()
            self.archivo_recibido.emit(full_path)



    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class caja_win:
    enviar_producto = Signal(str)
    
    def __init__(self, main_window):
        self.ui = main_window
        datos = {
            "paciente": "N/A",
            "medico": "N/A",
            "Total": 0,
            "servicios": []
        }
        self.ui.table_busq.hide()

        self.widget_nota = muestra_nota(datos)
        self.widget_nota.recibir_prod.connect(self.enviar_a_cuenta)
        self.ui.inv_comboBox.currentIndexChanged.connect(self.inventario)
        self.ui.inv_le.textChanged.connect(self.inventario)
        self.ui.venta_btn.clicked.connect(self.nueva_venta)

        self.ui.inv_le_2.textChanged.connect(self.busqueda)
        self.ui.inv_comboBox_2.currentIndexChanged.connect(self.busqueda)
        

        # Inicia el hilo de recepción TCP
        self.receiver = TCPReceiver("192.168.1.118", 8080)
        self.receiver.archivo_recibido.connect(self.procesar_archivo)
        self.receiver.start()


    def enviar_a_cuenta(self):
        self.ui.table_busq.hide()
        table_select_c = self.ui.inv_comboBox_2.currentText()
        seleccion = self.ui.table_busq.selectionModel()
        if seleccion.hasSelection():
            self.fila = seleccion.selectedIndexes()[0].row()
            if table_select_c  == "productos":
                code = self.ui.modelo_caja.index(self.fila,0).data()
                product = self.ui.modelo_caja.index(self.fila,1).data()
                price = self.ui.modelo_caja.index(self.fila,3).data() 
            elif table_select_c  == "servicios":
                code = self.ui.modelo_caja.index(self.fila,0).data()
                product = self.ui.modelo_caja.index(self.fila,1).data()
                price = self.ui.modelo_caja.index(self.fila,2).data() 

            #print(code_send,product_send,price_send)
            producto = {
                "Code" : code,
                "Item" : product,
                "Precio" : float(price)
            }
            #self.redibujar_tabla()

        else:
            print("nada seleccionado")
        
        #try:
         #   self.ui.add_btn_extra.clicked.disconnect()        #boton en widget
        #except TypeError:
         #   pass  # No había conexiones previas

        self.widget_nota.agregar_producto(producto)




    def closeEvent(self, event):
        self.receiver.stop()
        event.accept()



    def procesar_archivo(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as cuenta:
                datos = json.load(cuenta)
                print(datos.get("paciente"))
                print(datos.get("medico"))
                for servicio in datos.get("servicios", []):
                    print(servicio)
                print(datos.get("Total"))

            self.ui.HLayout.addWidget(self.widget_nota)  # Agrega el widget al layout

        except Exception as e:
            print(f"⚠️ Error al procesar el archivo {ruta}: {e}")



    def nueva_venta(self):
        #self.datos = "N/A"
        #nuevo_widget = muestra_nota(self.datos)
        self.ui.HLayout.addWidget(self.widget_nota)  # Agrega el widget al layout
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Código", "Servicio", "Precio"])
    


    def busqueda(self):
        #self.cuenta_Widget = muestra_nota(self.datos)
        if self.ui.inv_le_2.text() == '':
            self.ui.table_busq.hide()
        table_select_c = self.ui.inv_comboBox_2.currentText()
        search_value_c = self.ui.inv_le_2.text()

        self.ui.table_busq.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.table_busq.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.table_cuenta.setSelectionMode(QAbstractItemView.SingleSelection)        ##tabla de nota
        self.ui.table_cuenta.setSelectionBehavior(QAbstractItemView.SelectRows)         ##

        self.ui.modelo_caja = QtSql.QSqlQueryModel()
        if table_select_c == "productos":
            self.ui.modelo_caja.setQuery(f"SELECT CB,producto,stock,precio FROM productos where producto like '%{search_value_c}%' or CB like '%{search_value_c}%';")  # Consulta SQL
            self.ui.table_busq.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.ui.table_busq.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.ui.table_busq.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.ui.table_busq.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

            self.ui.modelo_caja.setHeaderData(0, Qt.Horizontal, "Código")
            self.ui.modelo_caja.setHeaderData(1, Qt.Horizontal, "Producto")                
            self.ui.modelo_caja.setHeaderData(2, Qt.Horizontal, "Stock")
            self.ui.modelo_caja.setHeaderData(3, Qt.Horizontal, "Precio")
            
        elif table_select_c == "servicios":
            self.ui.modelo_caja.setQuery(f"SELECT id, producto as Servicio,precio as Precio FROM servicios where producto like '%{search_value_c}%';")  # Consulta SQL
            self.ui.table_busq.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents) 
            self.ui.table_busq.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.ui.table_busq.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  

            self.ui.modelo_caja.setHeaderData(0, Qt.Horizontal, "ID")
            self.ui.modelo_caja.setHeaderData(1, Qt.Horizontal, "Servico")
            self.ui.modelo_caja.setHeaderData(2, Qt.Horizontal, "Precio")       

        if self.ui.modelo_caja.lastError().isValid():
            print("Error SQL:", self.ui.modelo_consul.lastError().text())
        if self.ui.table_busq:
            self.ui.table_busq.setModel(self.ui.modelo_caja)
            self.ui.table_busq.show()
        else:
            print("Error: no se encontró la tabla")
    

    



    def faltantes(self):
        self.ui.table_falt.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.table_falt.setSelectionBehavior(QAbstractItemView.SelectRows) 
        self.modelo_falt = QtSql.QSqlQueryModel()

        self.ui.table_falt.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.ui.table_falt.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.ui.table_falt.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.ui.table_falt.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

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





    def inventario(self):
        table_select = self.ui.inv_comboBox.currentText()
        search_value = self.ui.inv_le.text()

        self.ui.table_inv.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.table_inv.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.modelo_inv = QtSql.QSqlQueryModel()

        if table_select == "productos":
            self.modelo_inv.setQuery(
                f"SELECT CB,producto,stock,stock_min ,stock_max,precio FROM productos where producto like '%{search_value}%' or CB like '%{search_value}%';")

            self.modelo_inv.setHeaderData(0, Qt.Horizontal, "Código")
            self.modelo_inv.setHeaderData(1, Qt.Horizontal, "Producto")
            self.modelo_inv.setHeaderData(2, Qt.Horizontal, "Stock")
            self.modelo_inv.setHeaderData(3, Qt.Horizontal, "Stock Mínimo")
            self.modelo_inv.setHeaderData(4, Qt.Horizontal, "Stock Máximo")
            self.modelo_inv.setHeaderData(5, Qt.Horizontal, "Precio")

        elif table_select == "servicios":
            self.modelo_inv.setQuery(
                f"SELECT id, producto,precio FROM servicios where producto like '%{search_value}%';")

            self.modelo_inv.setHeaderData(0, Qt.Horizontal, "ID")
            self.modelo_inv.setHeaderData(1, Qt.Horizontal, "Producto")
            self.modelo_inv.setHeaderData(2, Qt.Horizontal, "Precio")

        if self.modelo_inv.lastError().isValid():
            print("Error SQL:", self.modelo_inv.lastError().text())

        if self.ui.table_inv:
            self.ui.table_inv.setModel(self.modelo_inv)
        else:
            print("Error: no se encontró la tabla")
