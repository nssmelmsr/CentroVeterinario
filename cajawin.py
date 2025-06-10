from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import *
from PySide6 import QtSql,QtWidgets
from cuentaWidget import Ui_cuenta_view
import socket , datetime, os, json



class muestra_nota(QWidget):

    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.ui = Ui_cuenta_view()
        self.ui.setupUi(self)

        self.ui.paciente_label_2.setText(datos.get("paciente", ""))
        self.ui.dr_label.setText(datos.get("medico", "")) ### cambiar a paciente
        self.ui.Total_label.setText(str(datos.get("total", "")))
        
        self.columnas = ["Codigo","Producto","Precio"]

        #self.ui.tableView.setColumnCount(len(self.columnas))
        #self.ui.tableView.setHorizontalHeaderLabels(self.columnas)

#        for i,fila in enumerate (datos.get("servicios")):
 #           for j, colummna in enumerate(self.columnas):
  #              item = QTableWidgetItem
   #             item.setData(Qt.EditRole, fila[colummna])
    #            self.ui.tableView.setItem(i,j,item)



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
    def __init__(self, main_window):
        self.ui = main_window

        self.ui.inv_comboBox.currentIndexChanged.connect(self.inventario)
        self.ui.inv_le.textChanged.connect(self.inventario)

        # Inicia el hilo de recepción TCP
        self.receiver = TCPReceiver("192.168.1.118", 8080)
        self.receiver.archivo_recibido.connect(self.procesar_archivo)
        self.receiver.start()

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
                print(datos.get("total"))


            nuevo_widget = muestra_nota(datos)
            self.ui.HLayout.addWidget(nuevo_widget)  # Agrega el widget al layout

        except Exception as e:
            print(f"⚠️ Error al procesar el archivo {ruta}: {e}")


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
