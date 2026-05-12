from flask import Flask, jsonify, request
import os
from variables import cargarvariables
from flask_wtf.csrf import CSRFProtect
from funciones_auxiliares import prepare_response_extra_headers

# -- configuracion de cabeceras seguras -- #
extra_headers=prepare_response_extra_headers(True)

def create_app():
    app = Flask(__name__)

    # configuración...
    app.config.setdefault('DEBUG', True)
    
    # configuración...
    app.config.from_pyfile('settings.py')
    csrf = CSRFProtect(app)

    @app.before_request
    def csrf_protect():
       # Excluye las rutas que empiecen por /login o /registro
       if not request.path.startswith("/login") and not request.path.startswith("/registro"):
           csrf.protect()

    # Importar y registrar blueprints aquí (evita side-effects en import)
    from rutas_usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

    from rutas_zapatos import bp as zapatos_bp
    app.register_blueprint(zapatos_bp, url_prefix='/api/zapatos')

    from rutas_ficheros import bp as ficheros_bp
    app.register_blueprint(ficheros_bp, url_prefix='/api/ficheros')

    from rutas_comentarios import bp as comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')

    @app.errorhandler(500)
    def server_error(error):
        print('An exception occurred during a request. ERROR:' + error, flush=True)
        ret={"status": "Internal Server Error"}
        return jsonify(ret), 500

    return app

if __name__ == '__main__':
    app=create_app()
    try:
        port = int(os.environ.get('PORT'))
        host = os.environ.get('HOST')
        app.run(host=host, port=port)
    except:
        print("Error starting server", flush=True)

