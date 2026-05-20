from __future__ import print_function
from flask import request,Blueprint, jsonify, g, make_response
import controlador_comentarios
from funciones_auxiliares import Encoder, prepare_response_extra_headers

bp = Blueprint('comentarios', __name__)

extra_headers = prepare_response_extra_headers(True)

@bp.route("/",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        comentario_json = g.cleaned_json
        usuario = comentario_json['usuario']
        descripcion = comentario_json['descripcion']
        respuesta,code= controlador_comentarios.insertar_comentario(usuario,descripcion)
    else:
        respuesta={"status":"Bad request"}
        code=401
        
    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

@bp.route("/",methods=['GET'])
def consultaComentarios():
    respuesta,code= controlador_comentarios.obtener_comentarios()
    
    response = make_response(jsonify(respuesta), code)
    response.headers.update(extra_headers)
    return response

