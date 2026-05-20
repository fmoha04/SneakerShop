from __future__ import print_function
from flask import request,Blueprint, jsonify, g, make_response
from funciones_auxiliares import Encoder, prepare_response_extra_headers
import controlador_usuarios

bp = Blueprint('usuarios', __name__)

extra_headers = prepare_response_extra_headers(True)

@bp.route("/login",methods=['POST'])
def login():
    if request.is_json:
        login_json = g.cleaned_json
        username = login_json['username']
        password = login_json['password']
        respuesta, code = controlador_usuarios.login_usuario(username, password)
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    # Crear respuesta y añadir cabeceras
    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

@bp.route("/registro",methods=['POST'])
def registro():
    if request.is_json:
        login_json = g.cleaned_json
        username = login_json['username']
        password = login_json['password']
        perfil = login_json.get('profile', 'normal')
        correo = login_json.get('correo', f"{username}@example.com")
        respuesta, code = controlador_usuarios.alta_usuario(username, password, perfil, correo)
    else:
        respuesta={"status":"Bad request"}
        code=401
    
    # Crear respuesta y añadir cabeceras
    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

@bp.route("/logout",methods=['GET'])
def logout():
    try:
        controlador_usuarios.logout()
        ret={"status":"OK"}
        code=200
    except Exception as e:
        print(f"Error en logout: {e}", flush=True)
        ret={"status":"ERROR"}
        code=500
        
    response=make_response(jsonify(ret),code)
    response.headers.update(extra_headers)
    return response

