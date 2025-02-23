import mysql.connector as sql

def connect_to_db():
    
    conexion = sql.connect(
        host = "localhost",
        user = "root",
        password = "Lademysql420.",
        database = "Veterinaria_v01",
        buffered = True
    )

    if conexion.is_connected():
        db_info = conexion.get_server_info
      #  conex.set_text("Conexión establecida")
        cursor = conexion.cursor()
        print("Server Version: ",db_info)
    else:
        #conex.set_text("No conectado") 
        print("No conectado")


    return conexion, cursor