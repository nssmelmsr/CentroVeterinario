from PySide6.QtWidgets import *
from PySide6 import  QtSql, QtWidgets
from PySide6.QtCore import Qt
import datetime
import json
import shutil
import os
import socket

class ConsWindow:
    def __init__(self,main_window):
        #super().__init__()
        #self.setupUi(self)
        self.ui = main_window # se guarda referencia a MainWindow
        self.columnas = ["Code","Item","Precio"]
        self.send = []                                  ##### lista para el  consultorio
        self.total = 0

        self.ui.exit_btn_2.clicked.connect(self.ui.close)    

        self.ui.wrong_dr.hide()
        self.ui.wrong_pet.hide()

        self.ui.busq_consul_le.textChanged.connect(self.consul_search)
        self.ui.consul_comboBox.currentIndexChanged.connect(self.consul_search)
        self.ui.remove_btn.clicked.connect(self.remove_item)
        self.ui.send_btn.clicked.connect(self.mandar_cuenta)

        self.time = datetime.datetime.now()
        self.carpeta = self.time.strftime("%d_%m_%Y")
        self.filename = "Nota_" + self.time.strftime("%H%M%S") + ".json"


    def consul_search(self):
        
        table_select_c = self.ui.consul_comboBox.currentText()
        search_value_c = self.ui.busq_consul_le.text()

        self.ui.busca_cuenta.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.busca_cuenta.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.table_cuenta.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.table_cuenta.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.ui.modelo_consul = QtSql.QSqlQueryModel()
        if table_select_c == "productos":
            self.ui.modelo_consul.setQuery(f"SELECT CB,producto,stock,precio FROM productos where producto like '%{search_value_c}%' or CB like '%{search_value_c}%';")  # Consulta SQL
            self.ui.busca_cuenta.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.ui.busca_cuenta.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.ui.busca_cuenta.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.ui.busca_cuenta.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

            self.ui.modelo_consul.setHeaderData(0, Qt.Horizontal, "Código")
            self.ui.modelo_consul.setHeaderData(1, Qt.Horizontal, "Producto")                
            self.ui.modelo_consul.setHeaderData(2, Qt.Horizontal, "Stock")
            self.ui.modelo_consul.setHeaderData(3, Qt.Horizontal, "Precio")
            
        elif table_select_c == "servicios":
            self.ui.modelo_consul.setQuery(f"SELECT id, producto as Servicio,precio as Precio FROM servicios where producto like '%{search_value_c}%';")  # Consulta SQL
            self.ui.busca_cuenta.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents) 
            self.ui.busca_cuenta.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.ui.busca_cuenta.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  

            self.ui.modelo_consul.setHeaderData(0, Qt.Horizontal, "ID")
            self.ui.modelo_consul.setHeaderData(1, Qt.Horizontal, "Servico")
            self.ui.modelo_consul.setHeaderData(2, Qt.Horizontal, "Precio")       


        if self.ui.modelo_consul.lastError().isValid():
            print("Error SQL:", self.ui.modelo_consul.lastError().text())
        if self.ui.busca_cuenta:
            self.ui.busca_cuenta.setModel(self.ui.modelo_consul)
        else:
            print("Error: no se encontró la tabla")
        

        try:
            self.ui.add_btn.clicked.disconnect()
        except TypeError:
            pass  # No había conexiones previas

        self.ui.add_btn.clicked.connect(self.add_cuenta)
        

    def remove_item(self):
        seleccion = self.ui.table_cuenta.selectionModel()
        fila = self.ui.table_cuenta.currentRow()
        if seleccion.hasSelection():
            #self.fila = seleccion.selectedIndexes()[0].row()
            self.send.pop(fila)  # elimina de la lista

            self.redibujar_tabla()

        else:
            print("No hay fila seleccionada para eliminar.")

    def add_cuenta(self):#, seleccion):
        table_select_c = self.ui.consul_comboBox.currentText()
        seleccion = self.ui.busca_cuenta.selectionModel()
        if seleccion.hasSelection():
            self.fila = seleccion.selectedIndexes()[0].row()
            if table_select_c  == "productos":
                code_send = self.ui.modelo_consul.index(self.fila,0).data()
                product_send = self.ui.modelo_consul.index(self.fila,1).data()
                price_send = self.ui.modelo_consul.index(self.fila,3).data() 
            elif table_select_c  == "servicios":
                code_send = self.ui.modelo_consul.index(self.fila,0).data()
                product_send = self.ui.modelo_consul.index(self.fila,1).data()
                price_send = self.ui.modelo_consul.index(self.fila,2).data() 

            print(code_send,product_send,price_send)
            self.send.append({
                "Code" : code_send,
                "Item" : product_send,
                "Precio" : price_send
            })
            self.redibujar_tabla()

        else:
            print("nada seleccionado")

    def redibujar_tabla(self):
        self.ui.wrong_dr.hide()
        self.ui.wrong_pet.hide()
        self.ui.table_cuenta.setRowCount(len(self.send))
        self.ui.table_cuenta.setColumnCount(len(self.columnas))
        self.ui.table_cuenta.setHorizontalHeaderLabels(self.columnas)


        for i, fila in enumerate(self.send):     #fila
            for j, columna in enumerate(self.columnas):     #columna
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, fila[columna]) #fila[columna]
                self.ui.table_cuenta.setItem(i,j,item)
        
        self.total = sum(item["Precio"] for item in self.send)
        self.ui.label_total.setText(f"Total: ${str(self.total)}")
        

    def  mandar_cuenta(self):
        if self.ui.paciente_le.text() == "":
            self.ui.wrong_pet.show()

        elif self.ui.mvz_comboBox.currentIndex() == 0:
            self.ui.wrong_dr.show()

        else:
            self.paciente = self.ui.paciente_le.text()
            self.medico = self.ui.mvz_comboBox.currentText()
            if os.path.exists(f"cuentas/{self.carpeta}"):

                #with open("cuentas/" + filename +  ".json", "w") as sendfile:
                with open(f"cuentas/{self.carpeta}/{self.filename}", "w") as sendfile:
                    json.dump({
                        "paciente" : self.paciente,
                        "medico" : self.medico,
                        "servicios" : self.send,
                        "Total" : self.total},sendfile)
                    sendfile.close()
                shutil.copy2(f"cuentas/{self.carpeta}/{self.filename}",f".cuentas_resp/{self.carpeta}/")
            else:
                os.mkdir(f"cuentas/{self.carpeta}")
                os.mkdir(f".cuentas_resp/{self.carpeta}")
                self.mandar_cuenta()
            self.ui.paciente_le.clear()
            self.send.clear()
            print(self.filename)

        self.redibujar_tabla()
        self.tcp_client()
    
    def tcp_client(self):  
        host = '192.168.1.80' ##IP de caja
        port = 8080
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        # Connecting with Server 
        sock.connect((host, port)) 
  
        #while True: 
        try: 
            # Reading file and sending data to server 
            fi = open(f"cuentas/{self.carpeta}/{self.filename}", "r") 
            data = fi.read() 
            #if not data: 
            #    break
            while data: 
                sock.send(str(data).encode()) 
                data = fi.read() 
            # File is closed after data is sent 
           # fi.close() 
            #exit()
        except IOError:
            print('no se encontró el archivo')
        #sock.close()
