from bd import obtener_conexion
import sys
import os
from funciones_auxiliares import calculariva, sanitize_field

def convertir_zapatos_a_json(zapato):
    
    d = {}
    d['id'] = zapato[0]
    d['nombre'] = sanitize_field(zapato[1])
    d['descripcion'] = sanitize_field(zapato[2])
    d['precio'] = float(zapato[3])
    d['precio_iva'] = float(zapato[4]) if zapato[4] else None
    d['foto'] = sanitize_field(zapato[5])
    d['marca'] = sanitize_field(zapato[6])
    return d

def insertar_zapato(nombre, descripcion, precio, foto, marca):
    
    conexion = None
    
    try:

        price_val = float(precio)
        precio_iva = price_val + calculariva(price_val)
        
        print(f"Inserting shoe: {nombre}, {descripcion}, {precio}, {precio_iva}, {foto}, {marca}", flush=True)
        
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:

            sql = """
                INSERT INTO zapatos (nombre, descripcion, precio, precio_iva, foto, marca) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (nombre, descripcion, price_val, float(precio_iva), foto, marca)
            cursor.execute(sql, params)
        
        conexion.commit()
        print("Shoe inserted successfully", flush=True)
        
        ret = {"status": "OK"}
        code = 200
        
    except Exception as e:

        if conexion:
            conexion.rollback()
            
        print(f"Error inserting shoe: {e}", flush=True)
        import traceback
        traceback.print_exc()
        
        ret = {"status": "Error", "mensaje": str(e)}
        code = 500
        
    finally:

        if conexion:
            conexion.close()
            
    return ret, code

def obtener_zapatos():
    
    zapatosjson = []
    
    try:
        conexion = obtener_conexion()
        
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio, precio_iva, foto, marca FROM zapatos")
            zapatos = cursor.fetchall()
            
            if zapatos:
                for zapato in zapatos:
                    zapatosjson.append(convertir_zapatos_a_json(zapato))
        
        conexion.close()
        code = 200
    
    except:
        print("Excepcion al consultar todas las zapatos", flush=True)
        code = 500
    
    return zapatosjson, code

def obtener_zapato_por_id(id):
    
    zapatojson = {}
    
    try:
        conexion = obtener_conexion()
        
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio, precio_iva, foto, marca FROM zapatos WHERE id = %s", (id,))
            zapato = cursor.fetchone()
            
            if zapato is not None:
                zapatojson = convertir_zapatos_a_json(zapato)
        conexion.close()
        code = 200
    
    except:
        print("Excepcion al consultar un zapato", flush=True)
        code = 500
    
    return zapatojson, code

def eliminar_zapato(id):
    
    try:
        conexion = obtener_conexion()
        
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM zapatos WHERE id = %s", (id,))
            
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            
            else:
                ret={"status": "Failure" }
        
        conexion.commit()
        conexion.close()
        code=200
    
    except:
        
        print("Excepcion al eliminar una zapato", flush=True)
        ret = {"status": "Failure" }
        code=500
    
    return ret,code

def actualizar_zapato(id, nombre, descripcion, precio, foto, marca):
    
    conexion = None
    
    try:
        price_val = float(precio)
        new_precio_iva = price_val + calculariva(price_val)
        conexion = obtener_conexion()
        
        with conexion.cursor() as cursor:
            sql = """
                UPDATE zapatos 
                SET nombre = %s, descripcion = %s, precio = %s, 
                    precio_iva = %s, foto = %s, marca = %s 
                WHERE id = %s
            """
            params = (nombre, descripcion, price_val, new_precio_iva, foto, marca, id)
            cursor.execute(sql, params)
            
            if cursor.rowcount == 1:
                conexion.commit()
                ret = {"status": "OK"}
                code = 200
            
            else:
                ret = {"status": "Failure", "mensaje": "Shoe not found or no changes applied"}
                code = 404

    except Exception as e:
        print(f"Exception while updating shoe: {e}", flush=True)
        
        if conexion:
            conexion.rollback()
        
        ret = {"status": "Failure", "mensaje": str(e)}
        code = 500
        
    finally:
        if conexion:
            conexion.close()
            
    return ret, code

