from __future__ import print_function
from flask import request,Blueprint, jsonify, g, make_response
from funciones_auxiliares import Encoder, prepare_response_extra_headers, validar_session_normal
import controlador_usuarios
import os

bp = Blueprint('usuarios', __name__)
extra_headers = prepare_response_extra_headers(True)

@bp.route("/login",methods=['POST'])

def login():
    
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        login_json = g.cleaned_json
        
        if "username" in login_json and "password" in login_json:
            username = login_json['username']
            password = login_json['password']
            
            if isinstance(username, str) and isinstance(password, str) and len(username) < 50 and len(password) < 50:
                respuesta, code = controlador_usuarios.login_usuario(username, password)
            else:
                respuesta = {"status": "Bad Parameters"}        
                code = 400
                
        else:
            respuesta = {"status": "Bad request", "mensaje": "Missing parameters"}
            code = 400
            
    else:
        respuesta = {"status": "Bad request", "mensaje": "Content-Type must be application/json"}
        code = 400 

    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

@bp.route("/registro", methods=['POST'])

def registro():
    
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        login_json = g.cleaned_json
        
        if "username" in login_json and "password" in login_json:
            username = login_json['username']
            password = login_json['password']
            perfil = login_json.get('profile', 'normal')
            correo = login_json.get('correo', f"{username}@example.com")
            
            if (isinstance(username, str) and isinstance(password, str) and 
                isinstance(perfil, str) and isinstance(correo, str) and
                len(username) < 50 and len(password) < 50 and 
                len(perfil) < 20 and len(correo) < 100):
                
                respuesta, code = controlador_usuarios.alta_usuario(username, password, perfil, correo)
            else:
                respuesta = {"status": "Bad parameters"}
                code = 400
                
        else:
            respuesta = {"status": "Bad request", "mensaje": "Missing parameters"}
            code = 400
            
    else:
        respuesta = {"status": "Bad request"}
        code = 400
    
    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

@bp.route("/logout", methods=['GET'])

def logout():
    
    if not validar_session_normal():
        ret = {"status": "Forbidden"}
        code = 403
        
    else:
        
        try:
            controlador_usuarios.logout()
            ret = {"status": "OK"}
            code = 200
            
        except Exception as e:
            print(f"Error en logout: {e}", flush=True)
            ret = {"status": "ERROR"}
            code = 500
        
    response = make_response(jsonify(ret), code)
    response.headers.update(extra_headers)
    return response

