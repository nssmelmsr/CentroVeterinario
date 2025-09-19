from PySide6.QtCore import Qt, QThread, Signal, QObject, Slot
from PySide6.QtWidgets import *
from PySide6 import QtSql,QtWidgets
from PySide6.QtGui import QStandardItemModel, QStandardItem
from cuentaWidget import Ui_cuenta_view
from getinfo import get_data
import socket , datetime, os, json, shutil  

class muestra_nota(QWidget):
    #recibir_prod = Signal(dict)
    recibir_prod = Signal(dict,object)     
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.ui = Ui_cuenta_view()

        self.ui.setupUi(self)
        self.columnas = ["Code", "Item", "Precio"]
        
        self.datos = []  

        self.ui.remove_btn_extra.clicked.connect(self.remove_item)
        self.ui.add_btn_extra.clicked.connect(self.recibir_pedido)
        self.ui.finish_btn.clicked.connect(self.cuenta_final)

        self.ui.paciente_label_2.setText(datos.get("paciente"))
        self.ui.dr_label.setText(datos.get("medico"))
        self.ui.Total_label.setText(f"${datos.get('Total', 0):.2f}")
        
        self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Convertimos los servicios iniciales en self.datos
        for servicio in datos.get("servicios", []):
            self.datos.append({
                "Code": servicio.get("Code", ""),
                "Item": servicio.get("Item", ""),
                "Precio": float(servicio.get("Precio", 0))
            })

        self.redibujar_tabla() 



    def recibir_pedido(self):
        self.recibir_prod.emit({}, self) 


    def cuenta_final(self):
        if self.ui.tarjCheckBox.isChecked() or self.ui.efeCheckBox.isChecked():
            self.guardar_nota()
        else: 
            print("seleccione método de pago")
            aviso = QMessageBox(self)
            aviso.setWindowTitle("¡Atención!")
            aviso.setText("Se requiere método de pago")
            aviso.exec()
            return

    def guardar_nota(self):

        now = datetime.datetime.now()
        self.paciente = self.ui.paciente_label_2.text()
        self.medico = self.ui.dr_label.text()
        if self.ui.efeCheckBox.isChecked() and self.ui.tarjCheckBox.isChecked():
            self.metodo = "pago con efectivo y tarjeta"
        elif self.ui.tarjCheckBox.isChecked():
            self.metodo = "pago con tarjeta"
        elif self.ui.efeCheckBox.isChecked():
            self.metodo = "pago con efectivo"
        self.extra = self.ui.notaLe.text()
        self.carpeta = now.strftime("%d_%m_%Y")
        self.filename = "Nota_" + now.strftime("%H%M%S") + ".json"

        os.makedirs(f"cuentas/{self.carpeta}", exist_ok=True)
        os.makedirs(f".cuentas_resp/{self.carpeta}", exist_ok=True)


            
        with open(f"cuentas/{self.carpeta}/{self.filename}", "w") as savefile:
                json.dump({
                    "paciente" : self.paciente,
                    "medico" : self.medico,
                    "servicios" : self.datos,
                    "pago" : self.metodo,
                    "extra" : self.extra,
                    "Total" : self.total},savefile)
                savefile.close()
        shutil.copy2(f"cuentas/{self.carpeta}/{self.filename}",f".cuentas_resp/{self.carpeta}")
        self.close()

            
        

    def redibujar_tabla(self):
        self.model = QStandardItemModel(len(self.datos), len(self.columnas))
        self.model.setHorizontalHeaderLabels(self.columnas)

        for i, fila in enumerate(self.datos):
            for j, columna in enumerate(self.columnas):
                valor = fila.get(columna, "")
                if columna == "Precio":
                    valor = f"${valor:.2f}"
                item = QStandardItem(str(valor))
                item.setData(valor, Qt.EditRole)
                self.model.setItem(i, j, item)

        self.ui.tableView.setModel(self.model)

        self.total = sum(f["Precio"] for f in self.datos)
        self.ui.Total_label.setText(f"Total: ${self.total:.2f}")

    def remove_item(self):
        seleccion = self.ui.tableView.selectionModel()
        if seleccion.hasSelection():
            fila = seleccion.selectedIndexes()[0].row()
            del self.datos[fila]  # <--- elimina del modelo lógico
            self.redibujar_tabla()
        else:
            print("No hay fila seleccionada para eliminar.")

    def agregar_producto(self, producto: dict):
        self.datos.append(producto)
        self.redibujar_tabla()

    def calcular_Total(self):
        return sum(p["Precio"] for p in self.datos)

    

class TCPReceiver(QThread):
    archivo_recibido = Signal(str)  # Emitirá la ruta del archivo recibido

    def __init__(self, parent=None):
        super().__init__(parent)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 8080
        self.running = True


    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(sock) 
        sock.bind((self.host, self.port))
        sock.listen(1)

        while self.running:
            conn, addr = sock.accept()
            print("Conectado con:", addr)
            now = datetime.datetime.now()
            carpeta = now.strftime("%d_%m_%Y")
            filename = "Nota_" + now.strftime("%H%M%S") + ".json"

            os.makedirs(f"tmp/{carpeta}", exist_ok=True)
            full_path = f"tmp/{carpeta}/{filename}"

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


class caja_win(QObject):
    enviar_producto = Signal(str)
    
    def __init__(self, main_window):
        datos = { 
            "paciente": "N/A",
            "medico": "N/A",
            "Total": 0,
            "servicios": []
        }
        self.ui = main_window

        self.ui.table_busq.hide()

        self.widget_nota = muestra_nota(datos)
        self.widget_nota.recibir_prod.connect(self.enviar_a_cuenta)
        self.ui.inv_comboBox.currentIndexChanged.connect(self.inventario)
        self.ui.inv_le.textChanged.connect(self.inventario)
        self.ui.venta_btn.clicked.connect(self.nueva_venta)

        self.ui.inv_le_2.textChanged.connect(self.busqueda)
        self.ui.inv_comboBox_2.currentIndexChanged.connect(self.busqueda)

        self.ui.tab_caja.currentChanged.connect(self._on_tab_changed)
        

        self.receiver = TCPReceiver()#self.host, self.port)
        self.receiver.archivo_recibido.connect(self.procesar_archivo)
        self.receiver.start()

    @Slot(str)  #################################


    

    def enviar_a_cuenta(self, info, widget): 
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

    
            producto = {
                "Code" : code,
                "Item" : product,
                "Precio" : float(price)
            }

            widget.agregar_producto(producto)
        else:
            print("nada seleccionado")
        



    def closeEvent(self, event):
        self.receiver.stop()
        event.accept()



    def procesar_archivo(self, ruta):
  #      from PySide6.QtWidgets import QLabel
   #     prueba = QLabel("Hola, soy una nota de prueba")
    #    prueba.setStyleSheet("background: yellow;")
     #   self.ui.HLayout.addWidget(prueba)
        try:
            with open(ruta, "r", encoding="utf-8") as cuenta:
                datos = json.load(cuenta)
                print(datos.get("paciente"))
                print(datos.get("medico"))
                for servicio in datos.get("servicios", []):
                    print(servicio)
                print(datos.get("Total"))
            
                nueva_nota = muestra_nota(datos)
                
                #nueva_nota.recibir_prod.connect(lambda info, w=nueva_nota: self.enviar_a_cuenta(info,w))
                nueva_nota.recibir_prod.connect(self.enviar_a_cuenta)
                ##############################
                if not hasattr(self, "notas_abiertas"):
                    self.notas_abiertas = []
                self.notas_abiertas.append(nueva_nota)

                # Asegurar que el layout es válido antes de añadir
                if hasattr(self.ui, "HLayout") and isinstance(self.ui.HLayout, QHBoxLayout):
                    self.ui.HLayout.addWidget(nueva_nota)
                else:
                    print("⚠️ Error: HLayout no es un QHBoxLayout válido o no existe en el .ui")

 
                ########################### bloque de prueba
                #self.ui.HLayout.addWidget(nueva_nota)      ##con este si jalaba
            #self.ui.HLayout.addWidget(self.widget_nota)  # Agrega el widget al layout

        except Exception as e:
            print(f"⚠️ Error al procesar el archivo {ruta}: {e}")



    def nueva_venta(self):

        datos = { 
            "paciente": "N/A",
            "medico": "N/A",
            "Total": 0,
            "servicios": []
        }
        nueva_nota = muestra_nota(datos)
        #nueva_nota.recibir_prod.connect(self.enviar_a_cuenta)
        nueva_nota.recibir_prod.connect(lambda info, w=nueva_nota: self.enviar_a_cuenta(info,w))
        self.ui.HLayout.addWidget(nueva_nota)
        self.widget_nota = nueva_nota  # actualizar la referencia para futuras operaciones
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
        #self.ui.table_cuenta.setSelectionMode(QAbstractItemView.SingleSelection)        ##tabla de nota
        #self.ui.table_cuenta.setSelectionBehavior(QAbstractItemView.SelectRows)         ##
        self.ui.table_busq.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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
            print("Error SQL:", self.ui.modelo_caja.lastError().text())
        if self.ui.table_busq:
            self.ui.table_busq.setModel(self.ui.modelo_caja)
            self.ui.table_busq.show()
        else:
            print("Error: no se encontró la tabla")



    def _on_tab_changed(self, idx):
        if self.ui.tab_caja.widget(idx) is self.ui.faltantes_tab:
            self.faltantes()


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
