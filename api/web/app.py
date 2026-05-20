from flask import Flask, jsonify, request
import os
# from variables import cargarvariables
from flask_wtf.csrf import CSRFProtect
from funciones_auxiliares import prepare_response_extra_headers
from logging.config import dictConfig

if not os.path.exists('logs'):
    os.makedirs('logs')

# -- configuracion de logging -- #
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "logs/flask.log",
                "formatter": "default",
            },
            "time-rotate": {
               "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "logs/flask.log",
                "when": "D",
                "interval": 10,
                "backupCount": 5,
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console","time-rotate"]},
    }

)

# -- configuracion de cabeceras seguras -- #
extra_headers=prepare_response_extra_headers(True)

def create_app():
    
    app = Flask(__name__)
    app.config.setdefault('DEBUG', True)
    app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('WTF_CSRF_SECRET_KEY', 'default_csrf_secret')
    
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    
#    app.config.from_pyfile('settings.py', silent=True)
    csrf = CSRFProtect(app)

    @app.after_request
    def after_request(response):
        response.headers['Server'] = 'API'
        app.logger.info(
            "path: %s | method: %s | status: %s | size: %s >>> %s",
            request.path,
            request.method,
            response.status,
            response.content_length,
            request.remote_addr,
        )
        response.headers.extend(extra_headers)
        return response

    @app.before_request
    def csrf_protect():
        if not request.path.startswith("/api/usuarios/login") and not request.path.startswith("/api/usuarios/registro") and not request.path.startswith("/api/comentarios"):
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
        port = int(os.environ.get('PORT', 5000))
        host = os.environ.get('HOST', '0.0.0.0')
        app.run(host=host, port=port)
    except:
        print("Error starting server", flush=True)

