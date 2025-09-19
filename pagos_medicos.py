import os
import json
from collections import Counter

directorio = "cuentas/pagos_prox/"

def filtrar_archivos_json(directorio):
    return [f for f in os.listdir(directorio) if f.endswith('.json') and os.path.isfile(os.path.join(directorio, f))]

def contar_medicos_en_consultas(directorio):
    archivos_json = filtrar_archivos_json(directorio)
    contador_medicos = Counter()
    for archivo in archivos_json:
        ruta = os.path.join(directorio, archivo)
        with open(ruta, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                for servicio in data.get("servicios", []):
                    consultas = servicio.get('Item', [])
                    if consultas == 'Consulta':
                        #for consulta in consultas:
                        medico = data.get('medico')
                        if medico:
                            print(f'Archivo: {archivo}, Médico: {medico}')
                            contador_medicos[medico] += 1
            except Exception as e:
                print(f'Error leyendo {archivo}: {e}')
    print('\nConteo de médicos:')
    for medico, cantidad in contador_medicos.items():
        print(f'{medico}: {cantidad}')

# Ejemplo de uso:
contar_medicos_en_consultas(directorio)