import os, json
from PySide6.QtWidgets import *
from getinfo import get_data


class admin_win:
    def __init__(self,main_window):
        self.ui = main_window # se guarda referencia a MainWindow
        ips = get_data()
        self.show_data(ips)
        self.ui.admin_SE_button.clicked.connect(self.guardar_cambios)


    def show_data(self,ips):
        caja = ips.get_caja()
        
        self.ui.IP_caja_le.setText(caja)
       # self.ui.IP_maq_le.setText(local)
    

    def guardar_cambios(self):
        if os.path.exists(f".myinf"):            
            with open(f".myinf/info.json", "w") as conffile:
                json.dump({
                    "IP_caja" : self.ui.IP_caja_le.text()},
    #                "IP_local" : self.ui.IP_maq_le.text()},
                    conffile)
                conffile.close()
        else:
            os.mkdir(f".myinf")
        self.ui.stackedWidget.setCurrentIndex(0)