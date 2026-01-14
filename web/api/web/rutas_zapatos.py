from flask import request, Blueprint, jsonify
import controlador_zapatos
from funciones_auxiliares import Encoder

bp = Blueprint('zapatos', __name__)

@bp.route("/",methods=["GET"])
def zapatos():
    respuesta,code= controlador_zapatos.obtener_zapatos()
    return jsonify(respuesta), code
    
@bp.route("/<id>",methods=["GET"])
def zapato_por_id(id):
    respuesta,code = controlador_zapatos.obtener_zapato_por_id(id)
    return jsonify(respuesta), code

@bp.route("/",methods=["POST"])
def guardar_zapato():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        zapato_json = request.json
        nombre = zapato_json["nombre"]
        descripcion = zapato_json["descripcion"]
        precio=zapato_json["precio"]
        foto=zapato_json["foto"]
        marca=zapato_json["marca"]
        respuesta,code=controlador_zapatos.insertar_zapato(nombre, descripcion,precio,foto,marca)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_zapato(id):
    respuesta,code=controlador_zapatos.eliminar_zapato(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_zapato():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        zapato_json = request.json
        id = zapato_json["id"]
        nombre = zapato_json["nombre"]
        descripcion = zapato_json["descripcion"]
        precio=float(zapato_json["precio"])
        foto=zapato_json["foto"]
        marca=zapato_json["marca"]
        respuesta,code=controlador_zapatos.actualizar_zapato(id,nombre,descripcion,precio,foto,marca)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code


