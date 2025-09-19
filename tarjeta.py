import os
import json

directorio = "cuentas/pagos_prox/"

def filtrar_archivos_json(directorio):
    return [f for f in os.listdir(directorio) if f.endswith('.json') and os.path.isfile(os.path.join(directorio, f))]

def metodo_de_pago(directorio):
    archivos_json = filtrar_archivos_json(directorio)
    
    for archivo in archivos_json:
        ruta = os.path.join(directorio, archivo)
        with open(ruta, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                pago = data.get("pago", [])
                total = data.get("Total", [])
                extra = data.get("extra", [])
                if (pago == 'pago con tarjeta') or (pago == "pago con efectivo y tarjeta"):
                    print("")
                    print(pago)
                    print(f'Archivo: {archivo}, Total: {total}')
                    for servicio in data.get("servicios", []):
                        item = servicio.get('Item', [])
                        precio = servicio.get('Precio', [])
                        print(f'{item}, {precio}')           
                    print(extra)
            
            except Exception as e:
                print(f'Error leyendo {archivo}: {e}')

metodo_de_pago(directorio)