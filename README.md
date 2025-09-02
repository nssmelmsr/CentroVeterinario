base de datos para veterinaria haciendo uso de MySQL server, python 3 y PyQt
para interfaz gráfica.

# Creado por nssmelmsr

## V0.3

Cambios en la interfaz gráfica, mayor tamaño de ventana.
más funciones en ventanas caja y consultorio.
Se agregan items a lista de compra en ventana consultorio

## V0.4

se crea ventana admin

## configuración previa

 se nececita crear un directorio con nombre ".myinf/"
 dentro de este hay dos archivos que se deben crear. "info.json" y ".my.cnf"

# info.json, debe tener el formato de tipo:
 
 {"IP_caja": "192.168.1.xxx"}

donde se deberá poner la ip del equipo que servira de caja

# .my.cnf deberá tener el formato:

[client]
user = tuUser
password = TuContraseña
host = tuHost

[mysql]
database = tuBaseDeDatos


