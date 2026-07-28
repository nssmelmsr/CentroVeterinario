import os,json
from PySide6.QtWidgets import QMessageBox
    
class get_data():
    #def __init__(self,main_window):
    
    def get_ip(self):
        if os.path.exists(f".myinf"): 
            with open(f".myinf/info.json", "r", encoding="utf-8") as data:
                info = json.load(data)        
                self.ip_caja = info.get("IP_caja")
                return self.ip_caja
        else: 
            print("cree archivo de configuración")
            aviso = QMessageBox(self)
            aviso.setWindowTitle("¡Atención!")
            aviso.setText("cree archivo de configuración")
            aviso.exec()

    def get_vet(self):
        if os.path.exists(f".myinf"): 
            with open(f".myinf/info.json", "r", encoding="utf-8") as data:
                info = json.load(data)        
                self.vet = info.get("veterinarios")
                return self.vet
        else: 
            print("cree archivo de configuración")
            aviso = QMessageBox(self)
            aviso.setWindowTitle("¡Atención!")
            aviso.setText("cree archivo de configuración")
            aviso.exec()        
    
    def get_local(self):
        if os.path.exists(f".myinf"): 
            with open(f".myinf/info.json", "r", encoding="utf-8") as data:
                info = json.load(data)        
                self.ip_local = info.get("IP_local")
                return self.ip_local
        else: 
            print("Falta método de pago")
            aviso = QMessageBox(self)
            aviso.setWindowTitle("¡Atención!")
            aviso.setText("Se requiere método de pago")
            aviso.exec()