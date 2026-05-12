from bd import obtener_conexion
import sys
import datetime as dt

# def login_usuario(username,password):
#     try:
#         conexion = obtener_conexion()
#         with conexion.cursor() as cursor:
#             cursor.execute("SELECT perfil FROM usuarios WHERE usuario = '" + username +"' and clave= '" + password + "'")
#             usuario = cursor.fetchone()
            
#             if usuario is None:
#                 ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
#             else:
#                 ret = {"status": "OK" }
#         code=200
#         conexion.close()
#     except:
#         print("Excepcion al validar al usuario", flush=True)   
#         ret={"status":"ERROR"}
#         code=500
#     return ret,code

# def alta_usuario(username,password,perfil):
#     try:
#         conexion = obtener_conexion()
#         with conexion.cursor() as cursor:
#             cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s",(username,))
#             usuario = cursor.fetchone()
#             if usuario is None:
#                 cursor.execute("INSERT INTO usuarios(usuario,clave,perfil) VALUES('"+ username +"','"+  password+"','"+ perfil+"')")
#                 if cursor.rowcount == 1:
#                     conexion.commit()
#                     ret={"status": "OK" }
#                     code=200
#                 else:
#                     ret={"status": "ERROR" }
#                     code=500
#             else:
#                 ret = {"status": "ERROR","mensaje":"Usuario ya existe" }
#                 code=200
#         conexion.close()
#     except:
#         print("Excepcion al registrar al usuario", flush=True)   
#         ret={"status":"ERROR"}
#         code=500
#     return ret,code    

# def logout():
#     return {"status":"OK"},200

# / implementacion codigo seguro anti-vulnerabilidades

def login_usuario(username,passwordIn):
    try:
        conexion = obtener_conexion()

        sql = "SELECT perfil FROM usuarios WHERE usuario = %s AND clave = %s"
        values = (username, password)

        with conexion.cursor() as cursor:
            cursor.execute(sql, values)
            resultado = cursor.fetchone()
            
            if resultado:
                ret = {"status": "OK" }
            else : 
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
        code=200
        conexion.close()
    except Exception as e:
        print(f"Excepcion al validar al usuario: {e}", flush=True)   
        ret={"status":"ERROR"}
        code=500
    return ret,code

def alta_usuario(username, password, perfil):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT 1 FROM usuarios WHERE usuario = %s", (username,))
            if cursor.fetchone() is None:
                
                sql_insert = "INSERT INTO usuarios (usuario, clave, perfil) VALUES (%s, %s, %s)"
                valores = (username, password, perfil)
                cursor.execute(sql_insert, valores)
                
                conexion.commit()
                ret = {"status": "OK"}
                code = 200
            else:
                ret = {"status": "ERROR", "mensaje": "Usuario ya existe"}
                code = 409  
                
    except Exception as e:
        print(f"Excepcion al registrar al usuario: {e}", flush=True)
        if conexion:
            # Undo changes 
            conexion.rollback() 
        ret = {"status": "ERROR", "mensaje": "Error interno del servidor"}
        code = 500
    finally:
        if conexion:
            conexion.close()
            
    return ret, code
