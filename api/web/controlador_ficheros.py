from __future__ import print_function
import os
import sys
import subprocess


def guardar_fichero(nombre,contenido):
    try:
        print(nombre, flush=True)
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        print(basepath, flush=True)
        ruta_archivos = os.path.join(basepath, 'static/archivos')
        
        # Crear directorio si no existe
        if not os.path.exists(ruta_archivos):
            os.makedirs(ruta_archivos)
            print(f"Directorio creado: {ruta_archivos}", flush=True)
        
        ruta_fichero = os.path.join(ruta_archivos, nombre)
        print('Archivo guardado en ' + ruta_fichero, flush=True)
        contenido.save(ruta_fichero)
        respuesta={"status": "OK"}
        code=200
    except Exception as e:
        print(f"Excepcion al guardar el fichero: {e}", flush=True)  
        respuesta={"status": "ERROR"}
        code=500
    return respuesta, code

def ver_fichero(nombre):
    try:
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        ruta_fichero = os.path.join(basepath, 'static/archivos', nombre)
        
        print(f"Intentando leer archivo: {ruta_fichero}", flush=True)
        
        # Verificar que el archivo existe
        if not os.path.exists(ruta_fichero):
            print(f"Archivo no encontrado: {ruta_fichero}", flush=True)
            respuesta = {"status": "ERROR", "contenido": "Archivo no encontrado"}
            return respuesta, 404
        
        # Leer el archivo
        with open(ruta_fichero, 'r', encoding='utf-8') as f:
            salida = f.read()
        
        respuesta = {"status": "OK", "contenido": salida}
        code = 200
        
    except Exception as e:
        print(f"Excepcion al ver el fichero: {e}", flush=True)   
        respuesta = {"status": "ERROR", "contenido": f"Error: {str(e)}"}
        code = 500
    return respuesta, code

def listar_ficheros():
    try:
        basepath = os.path.dirname(__file__)
        ruta_archivos = os.path.join(basepath, 'static/archivos')
        
        # Crear directorio si no existe
        if not os.path.exists(ruta_archivos):
            os.makedirs(ruta_archivos)
            return [], 200
        
        # Obtener lista de archivos
        archivos = os.listdir(ruta_archivos)
        archivos = [f for f in archivos if os.path.isfile(os.path.join(ruta_archivos, f))]
        
        respuesta = archivos
        code = 200
    except Exception as e:
        print(f"Excepcion al listar ficheros: {e}", flush=True)
        respuesta = []
        code = 500
    return respuesta, code


