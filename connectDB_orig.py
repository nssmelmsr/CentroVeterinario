from PySide6.QtSql import QSqlDatabase

def conectarDB():
    """Conecta a la base de datos MySQL y devuelve la conexión."""
    db = QSqlDatabase.addDatabase("QMYSQL")  # Especificamos el driver de MySQL
    db.setHostName("localhost")  # Servidor
    db.setDatabaseName("Veterinaria_v01")  # Nombre de la base de datos
    db.setUserName("root")  # Usuario de la base de datos
    db.setPassword("Lademysql420.")  # Contraseña

    if not db.open():
        print("Error: No se pudo conectar a la base de datos.")
        return None
    elif db.open():
        print("Conectado a la base de datos.")
    return db