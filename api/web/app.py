from flask import Flask, jsonify, request, g
import os
from flask_wtf.csrf import CSRFProtect, generate_csrf
from logging.config import dictConfig
from funciones_auxiliares import sanitize_field, prepare_response_extra_headers

if not os.path.exists("logs"):
    os.makedirs("logs")

dictConfig({
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
        "time-rotate": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/flask.log",
            "when": "D",
            "interval": 10,
            "backupCount": 5,
            "formatter": "default",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console", "time-rotate"]},
})

csrf = CSRFProtect()

extra_headers = prepare_response_extra_headers(True)

def create_app():
    
    app = Flask(__name__)

    app.config.setdefault('DEBUG', True)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))
    app.config['WTF_CSRF_TIME_LIMIT'] = None
    app.config.update(
        PERMANENT_SESSION_LIFETIME=600,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=True
    )

    csrf.init_app(app)

    @app.before_request
    def clean_request():
        g.cleaned_json = {}
        if request.is_json:
            data = request.get_json(silent=True)
            if data is not None:
                g.cleaned_json = sanitize_field(data)

    from rutas_usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    csrf.exempt(usuarios_bp)

    from rutas_zapatos import bp as zapatos_bp
    app.register_blueprint(zapatos_bp, url_prefix='/api/zapatos')

    from rutas_ficheros import bp as ficheros_bp
    app.register_blueprint(ficheros_bp, url_prefix='/api/ficheros')

    from rutas_comentarios import bp as comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')
    csrf.exempt(comentarios_bp)

    @app.after_request
    def after_request_handler(response):
        
        response.headers['Server'] = 'API'
        response.headers.extend(extra_headers)
        
        response.set_cookie('csrf_token', generate_csrf(), samesite='Lax')
        
        app.logger.info(
            "path: %s | method: %s | status: %s | size: %s >>> %s",
            request.path, request.method, response.status, 
            response.content_length, request.remote_addr
        )
        return response

    @app.errorhandler(500)
    def server_error(error):
        app.logger.error(f'An exception occurred: {error}')
        return jsonify({"status": "Internal Server Error"}), 500

    return app

if __name__ == '__main__':
    app=create_app()
    try:
        port = int(os.environ.get('PORT', 5000))
        host = os.environ.get('HOST', '0.0.0.0')
        app.run(host=host, port=port, ssl_context=('/app/certs/cert.pem', '/app/certs/key.pem'))
    except Exception as e:
        print(f"Error starting server: {e}", flush=True)

