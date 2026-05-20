from flask import Flask, jsonify, request, g
from flask_wtf.csrf import CSRFProtect
import os
from funciones_auxiliares import sanitize_field

csrf = CSRFProtect()

def create_app():
    
    app = Flask(__name__)

    # Config
    app.config.setdefault('DEBUG', True)
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY']= SECRET_KEY
    app.config['WTF_CSRF_TIME_LIMIT'] = None

    csrf.init_app(app)

    @app.before_request
    def clean_request():
        g.cleaned_json = {}
        if request.is_json:
            data = request.get_json(silent=True)
            if data is not None:
               g.cleaned_json = sanitize_field(data)

    # Importar y registrar blueprints aquí (evita side-effects en import)
    from rutas_usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    csrf.exempt(usuarios_bp)

    from rutas_zapatos import bp as zapatos_bp
    app.register_blueprint(zapatos_bp, url_prefix='/api/zapatos')

    from rutas_ficheros import bp as ficheros_bp
    app.register_blueprint(ficheros_bp, url_prefix='/api/ficheros')

    from rutas_comentarios import bp as comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')

    @app.after_request
    def set_csrf_cookie(response):
        # Genera un token CSRF y lo guarda en una cookie llamada 'csrf_token'
        from flask_wtf.csrf import generate_csrf
        response.set_cookie('csrf_token', generate_csrf(), samesite='Lax')
        return response

    @app.errorhandler(500)
    def server_error(error):
        print(f'An exception occurred during a request. ERROR: {error}', flush=True)
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

