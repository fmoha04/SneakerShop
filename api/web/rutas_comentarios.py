from __future__ import print_function
from flask import request, Blueprint, jsonify, g, make_response
import controlador_comentarios
import os
from funciones_auxiliares import Encoder, prepare_response_extra_headers
from funciones_auxiliares import validar_session_normal

bp = Blueprint('comentarios', __name__)

extra_headers = prepare_response_extra_headers(True)

@bp.route("/", methods=['GET'])

def obtener():
    
    if not validar_session_normal():
        respuesta = {"status": "Forbidden"}
        code = 403
        
    else:
        respuesta, code = controlador_comentarios.obtener_comentarios()
        
    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

@bp.route("/", methods=['POST'])

def insertar():
    
    if not validar_session_normal():
        respuesta = {"status": "Forbidden"}
        code = 403
    
    else:
        content_type = request.headers.get('Content-Type')
        
        if content_type == 'application/json':
            comentario_json = g.cleaned_json
            
            if "usuario" in comentario_json and "descripcion" in comentario_json:
                usuario = comentario_json['usuario']
                descripcion = comentario_json['descripcion']
                
                if (isinstance(usuario, str) and isinstance(descripcion, str) and 
                    len(usuario) < 50 and len(descripcion) < 500):
                    respuesta, code = controlador_comentarios.insertar_comentario(usuario, descripcion)
                
                else:
                    respuesta = {"status": "Bad parameters"}
                    code = 400
                    
            else:
                respuesta = {"status": "Bad parameters"}
                code = 400
        else:
            respuesta = {"status": "Bad request"}
            code = 400
            
    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

