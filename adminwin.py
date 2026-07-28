import os, json
from PySide6.QtWidgets import *
from getinfo import get_data


class admin_win:
    def __init__(self, main_window):
        self.ui = main_window
        ips = get_data()
        self.show_data(ips)
        self.ui.admin_add_dr.clicked.connect(self.add_vet)
        self.ui.admin_rmv_dr.clicked.connect(self.rmv_vet)
        self.ui.admin_SE_button.clicked.connect(self.guardar_cambios)



    def show_data(self, ips):
        caja = ips.get_ip()
        veterinarios = ips.get_vet()

        self.ui.IP_caja_le.setText(caja)
        self.ui.listWidget.addItems(veterinarios)

    def add_vet(self):
        dialog = QInputDialog(self.ui)
        dialog.setWindowTitle("Agregar veterinario")
        dialog.setLabelText("Nombre del M.V.Z.:")
        dialog.resize(350, 150)

        if dialog.exec():
            texto = dialog.textValue().strip()

            if texto:
                self.ui.listWidget.addItem(f"M.V.Z. {texto}")
        
    def rmv_vet(self):
        item = self.ui.listWidget.currentItem()

        if item is not None:
            self.ui.listWidget.takeItem(self.ui.listWidget.row(item))

    def guardar_cambios(self):

        # si no existe la carpeta la crea
        if not os.path.exists(".myinf"):
            os.mkdir(".myinf")

        #diccionario por defecto
        datos = {}

        #si ya existe el archivo, carga lo que tenga
        if os.path.exists(".myinf/info.json"):
            with open(".myinf/info.json", "r", encoding="utf-8") as conffile:
                datos = json.load(conffile)

        # Se actualiza únicamente la IP
        datos["IP_caja"] = self.ui.IP_caja_le.text()

        # guardar también los veterinarios
        veterinarios = []

        for i in range(self.ui.listWidget.count()):
            veterinarios.append(
                self.ui.listWidget.item(i).text()
            )
        datos["veterinarios"] = veterinarios


        with open(".myinf/info.json", "w", encoding="utf-8") as conffile:
            json.dump(datos, conffile, indent=4, ensure_ascii=False)

        self.ui.stackedWidget.setCurrentIndex(0)
