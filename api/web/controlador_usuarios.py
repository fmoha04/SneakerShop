from bd import obtener_conexion
import sys
import datetime as dt
from flask import current_app as app 
from flask_wtf.csrf import generate_csrf
from utils_passwords import cipher_password, compare_password

def create_session(username, perfil):
    """Create user session"""
    pass

def login_usuario(username,passwordIn):
    try:
        conexion = obtener_conexion()

        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil,clave,numeroAccesosErroneo FROM usuarios WHERE estado='activo' and usuario = %s",(username,))
            usuario = cursor.fetchone()
            
            if usuario is None:
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
            else:
                perfil = usuario[0]
                password = usuario[1]
                numAccesosErroneos = usuario[2]
                
                current_date = dt.date.today()
                hoy = current_date.strftime('%Y-%m-%d')
                
                if compare_password(password, passwordIn):
                    ret = {"status": "OK",
                           "csrf_token": generate_csrf(),
                           "perfil": perfil}
                    app.logger.info("Acceso usuario %s correcto", username)
                    create_session(username, perfil)
                    numAccesosErroneos = 0
                    estado = 'activo'
                else:
                    app.logger.info("Acceso usuario %s incorrecto", username)
                    numAccesosErroneos = numAccesosErroneos + 1
                    if numAccesosErroneos > 2:
                        estado = "bloqueado"
                        app.logger.info("Usuario %s bloqueado", username)
                    else:
                        estado = 'activo'
                    ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo"}
                
                cursor.execute("UPDATE usuarios SET numeroAccesosErroneo=%s, fechaUltimoAcceso=%s, estado=%s WHERE usuario = %s",(numAccesosErroneos, hoy, estado, username))
                conexion.commit()
            
            conexion.close()
        code = 200
    except Exception as e:
        print(f"Excepcion al validar al usuario: {e}", flush=True)   
        ret = {"status":"ERROR"}
        code = 500
    return ret, code

def alta_usuario(username, password, correo):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s", (username,))
            usuario = cursor.fetchone()
            
            if usuario is None:
                passwordC = cipher_password(password)
                cursor.execute(
                    "INSERT INTO usuarios(usuario, clave, correo, perfil, estado, numeroAccesosErroneo) VALUES(%s, %s, %s, 'normal', 'activo', 0)",
                    (username, passwordC, correo))

                if cursor.rowcount == 1:
                    conexion.commit()
                    app.logger.info("Nuevo usuario creado")
                    ret = {"status": "OK"}
                    code = 200
                else:
                    ret = {"status": "ERROR"}
                    code = 500
            else:
                ret = {"status": "ERROR", "mensaje": "Usuario ya existe"}
                code = 200
                
    except Exception as e:
        print(f"Excepcion al registrar al usuario: {e}", flush=True)
        if conexion:
            conexion.rollback()
        ret = {"status": "ERROR"}
        code = 500
    finally:
        if conexion:
            conexion.close()
            
    return ret, code

