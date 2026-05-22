from funciones_auxiliares import cipher_password, compare_password, create_session, delete_session
from bd import obtener_conexion
import os
import sys
import datetime as dt
from flask import current_app
from flask_wtf.csrf import generate_csrf

def logout():
    try:
        delete_session()
        return {"status": "OK"}, 200
    except:
        return {"status": "ERROR"}, 500

def login_usuario(username,passwordIn):
    try:
        conexion = obtener_conexion()

        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil,clave,numeroAccesosErroneo FROM usuarios WHERE estado='activo' and usuario = %s",(username,))
            usuario = cursor.fetchone()
            
            if usuario is None:
                
                current_app.logger.warning(f"Intento acceso con usuario no encontrado: {username}")
                
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
                code = 200
            else:
                perfil = usuario[0]
                password_hash = usuario[1]
                numAccesosErroneos = usuario[2]
                
                current_date = dt.date.today()
                hoy = current_date.strftime('%Y-%m-%d')
                
                if compare_password(password_hash, passwordIn):
                    ret = {"status": "OK", "csrf_token": generate_csrf(), "perfil": perfil}
                    
                    current_app.logger.info(f"Acceso usuario {username} correcto")
                    
                    create_session(username, perfil)
                    numAccesosErroneos = 0
                    estado = 'activo'
                else:
                    
                    current_app.logger.warning(f"Acceso usuario {username} incorrecto")
                    
                    numAccesosErroneos += 1
                    if numAccesosErroneos > 2:
                        estado = 'bloqueado'
                    
                        current_app.logger.error(f"Usuario {username} bloqueado por mala persona")
                    
                    else:
                        estado = 'activo'
                    ret = {"status": "ERROR", "mensaje": "Usuario/Clave erroneo"}
                
                cursor.execute("UPDATE usuarios SET numeroAccesosErroneo=%s, fechaUltimoAcceso=%s, estado=%s WHERE usuario = %s",(numAccesosErroneos, hoy, estado, username))
                conexion.commit()

            conexion.close()
        code = 200

    except Exception as e:
        print(f"Excepcion al validar al usuario: {e}", flush=True)   
        ret = {"status":"ERROR"}
        code = 500
    return ret, code

def alta_usuario(username, password, perfil, correo):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s", (username,))
            usuario = cursor.fetchone()
            
            if usuario is None:
                passwordC = cipher_password(password)
                cursor.execute(
                    "INSERT INTO usuarios(usuario, clave, correo, perfil, estado, numeroAccesosErroneo) VALUES(%s, %s, %s, %s, 'activo', 0)", 
                    (username, passwordC, correo, perfil))

                if cursor.rowcount == 1:
                    conexion.commit()
                    current_app.logger.info("Nuevo usuario creado")
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

