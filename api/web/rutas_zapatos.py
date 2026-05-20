from flask import request, Blueprint, jsonify, g
import controlador_zapatos
from funciones_auxiliares import Encoder
import os
from werkzeug.utils import secure_filename

bp = Blueprint('zapatos', __name__)

# Directorio para guardar archivos
UPLOAD_FOLDER = '/tmp/zapatos_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff', 'svg', 'doc', 'docx', 'xlsx', 'zip', 'rar'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/", methods=["GET"])
def zapatos():
    respuesta, code = controlador_zapatos.obtener_zapatos()
    return jsonify(respuesta), code
    
@bp.route("/<id>", methods=["GET"])
def zapato_por_id(id):
    respuesta, code = controlador_zapatos.obtener_zapato_por_id(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["POST"])
def guardar_zapato():
    try:
        print("=== GUARDANDO ZAPATO ===", flush=True)
        content_type = request.headers.get('Content-Type')
        print(f"Content-Type: {content_type}", flush=True)
        print(f"Form data: {request.form}", flush=True)
        print(f"Files: {request.files}", flush=True)
        
        # Manejo de multipart/form-data (con archivo)
        if content_type and 'multipart/form-data' in content_type:
            nombre = request.form.get("nombre")
            descripcion = request.form.get("descripcion")
            precio = request.form.get("precio")
            marca = request.form.get("marca")
            
            print(f"Datos recibidos: nombre={nombre}, desc={descripcion}, precio={precio}, marca={marca}", flush=True)
            
            # Validar campos requeridos
            if not all([nombre, descripcion, precio, marca]):
                print("Error: Faltan campos requeridos", flush=True)
                return jsonify({"status": "Bad request", "mensaje": "Faltan campos requeridos"}), 400
            
            # Procesar archivo
            foto = None
            if 'foto' in request.files:
                file = request.files['foto']
                print(f"Archivo recibido: {file.filename}", flush=True)
                if file and file.filename != '':
                    if allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(UPLOAD_FOLDER, filename)
                        file.save(filepath)
                        foto = filename
                        print(f"Archivo guardado como: {foto}", flush=True)
                    else:
                        print(f"Tipo de archivo no permitido: {file.filename}", flush=True)
                        return jsonify({"status": "Bad request", "mensaje": "Tipo de archivo no permitido"}), 400
            
            if not foto:
                print("Error: No se proporcionó archivo", flush=True)
                return jsonify({"status": "Bad request", "mensaje": "El archivo de foto es requerido"}), 400
            
            print(f"Llamando a insertar_zapato con: {nombre}, {descripcion}, {precio}, {foto}, {marca}", flush=True)
            respuesta, code = controlador_zapatos.insertar_zapato(
                nombre, descripcion, precio, foto, marca
            )
            print(f"Respuesta de insertar_zapato: {respuesta}, {code}", flush=True)
        # Manejo de JSON (sin archivo)
        elif content_type == 'application/json':
            zapato_json = g.cleaned_json
            nombre = zapato_json.get("nombre")
            descripcion = zapato_json.get("descripcion")
            precio = zapato_json.get("precio")
            foto = zapato_json.get("foto")
            marca = zapato_json.get("marca")
            
            respuesta, code = controlador_zapatos.insertar_zapato(
                nombre, descripcion, precio, foto, marca
            )
        else:
            print(f"Content-Type no reconocido: {content_type}", flush=True)
            respuesta = {"status": "Bad request"}
            code = 400
            
    except Exception as e:
        print(f"Error al guardar zapato: {e}", flush=True)
        import traceback
        traceback.print_exc()
        respuesta = {"status": "Error", "mensaje": str(e)}
        code = 500
        
    return jsonify(respuesta), code

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_zapato(id):
    respuesta, code = controlador_zapatos.eliminar_zapato(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_zapato():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        zapato_json = g.cleaned_json
        id = zapato_json["id"]
        nombre = zapato_json["nombre"]
        descripcion = zapato_json["descripcion"]
        precio = float(zapato_json["precio"])
        foto = zapato_json["foto"]
        marca = zapato_json["marca"]
        respuesta, code = controlador_zapatos.actualizar_zapato(
            id, nombre, descripcion, precio, foto, marca
        )
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    return jsonify(respuesta), code


