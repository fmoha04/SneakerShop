from bd import obtener_conexion
import sys


def convertir_zapatos_a_json(zapato):
    d = {}
    d['id'] = zapato[0]
    d['nombre'] = zapato[1]
    d['descripcion'] = zapato[2]
    d['precio'] = float(zapato[3])
    d['foto'] = zapato[4]
    d['marca']=zapato[5]
    return d

def insertar_zapato(nombre, descripcion, precio,foto,marca):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO zapatos(nombre, descripcion, precio,foto,marca) VALUES (%s, %s, %s,%s,%s)",
                       (nombre, descripcion, precio,foto,marca))
    conexion.commit()
    conexion.close()
    ret={"status": "OK" }
    code=200
    return ret,code

def obtener_zapatos():
    zapatosjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,marca FROM zapatos")
            zapatos = cursor.fetchall()
            if zapatos:
                for zapato in zapatos:
                    zapatosjson.append(convertir_zapatos_a_json(zapato))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas las zapatos", flush=True)
        code=500
    return zapatosjson,code

def obtener_zapato_por_id(id):
    zapatojson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio,foto,marca FROM zapatos WHERE id =" + id)
            zapato = cursor.fetchone()
            if zapato is not None:
                zapatojson = convertir_zapato_a_json(zapato)
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar un zapato", flush=True)
        code=500
    return zapatojson,code
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

def actualizar_zapato(id, nombre, descripcion, precio, foto,marca):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE zapatos SET nombre = %s, descripcion = %s, precio = %s, foto=%s, marca=%s WHERE id = %s",
                       (nombre, descripcion, precio, foto,marca,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al actualizar un zapato", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code

