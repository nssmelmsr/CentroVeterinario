from PySide6.QtSql import QSqlDatabase
import configparser

def conectarDB():
    reader = configparser.RawConfigParser()
    reader.read(".myinf/.my.cnf")

    #Conecta a la base de datos MySQL y devuelve la conexión.#
    db = QSqlDatabase.addDatabase("QMYSQL")  # Especificamos el driver de MySQL

    db.setHostName(reader.get('client','host'))  # Servidor
    db.setDatabaseName(reader.get('mysql','database'))  # Nombre de la base de datos
    db.setUserName(reader.get('client','user'))  # Usuario de la base de datos
    db.setPassword(reader.get('client','password'))  # Contraseña


    if not db.open():
        print("Error: No se pudo conectar a la base de datos.")
        return None
    elif db.open():
        print("Conectado a la base de datos.")
    return db