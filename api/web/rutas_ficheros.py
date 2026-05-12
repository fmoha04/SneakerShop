from __future__ import print_function
from flask import request,Blueprint, jsonify, make_response
from funciones_auxiliares import prepare_response_extra_headers
import controlador_ficheros
import os
import sys
import subprocess
from flask_wtf.csrf import CSRFProtect
from app import app 

csrf = CSRFProtect(app)

bp = Blueprint('ficheros', __name__)

extra_headers = prepare_response_extra_headers(True)

@bp.route ('/', methods=['GET'])
@csrf.exempt
def listar():
    try:
        respuesta, code = controlador_ficheros.listar_ficheros()
    except Exception as e:
        print(f"Error listando archivos: {e}", flush=True)
        respuesta = []
        code = 500
    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

@bp.route ('/', methods=['POST']) 
@csrf.exempt
def upload():
    try:
        contenido= request.files['fichero'] 
        nombre = request.form.get("nombre")
        respuesta,code = controlador_ficheros.guardar_fichero(nombre,contenido)
    except Exception as e:
        print(f"Error subiendo archivo: {e}", flush=True)
        respuesta={"status": "ERROR"}
        code=500
    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

@bp.route ('/<archivo>', methods=['GET']) 
@csrf.exempt
def ver(archivo):
    try:
        respuesta,code = controlador_ficheros.ver_fichero(archivo)
    except:
        respuesta= {"status": "ERROR"}
        code=500
    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

