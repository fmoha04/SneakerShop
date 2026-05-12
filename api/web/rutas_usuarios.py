from __future__ import print_function
from flask import request,Blueprint, jsonify, make_response
from funciones_auxiliares import Encoder, prepare_response_extra_headers
import controlador_usuarios

bp = Blueprint('usuarios', __name__)

extra_headers = prepare_response_extra_headers(True)

@bp.route("/login",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
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
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        username = login_json['username']
        password = login_json['password']
        profile = login_json['profile']
        respuesta,code= controlador_usuarios.alta_usuario(username,password,profile)
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
        controlador_usuarios.logout()()
        ret={"status":"OK"}
        code=200
    except:
        ret={"status":"ERROR"}
        code=500
    response=make_response(jsonify(ret),code)
    response.headers.update(extra_headers)
    return response

