base de datos para veterinaria haciendo uso de MySQL server, python 3 y PyQt
para interfaz gráfica.

## V0.45

Se pueden agregar y quitar doctores en ventana admin

## Configuración previa

 se nececita crear un directorio con nombre ".myinf/"
 dentro de este hay dos archivos que se deben crear. "info.json" y ".my.cnf"

# info.json, debe tener el formato de tipo:
 
 {
    IP_caja": "192.168.1.xxx",
    "veterinarios": []
 }

IP_caja: la ip del equipo que servira de caja 


# .my.cnf deberá tener el formato:

[client]
user = tuUser
password = TuContraseña
host = tuHost

[mysql]
database = tuBaseDeDatos


