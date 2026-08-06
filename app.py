import os
import webbrowser
from flask import Flask
from backend.config import Config
from backend.models.usuario import db
from backend.controllers.auth_controller import auth_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, 'html'),
    static_folder=FRONTEND_DIR,
    static_url_path='/static'
)
app.config.from_object(Config)

# Inicializa o SQLAlchemy com as configurações do app
db.init_app(app)

# Registra as rotas da Controller de Autenticação
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    # Cria as tabelas se elas não existirem (não apaga os dados existentes)
    with app.app_context():
        db.create_all()

    # Abre o navegador automaticamente, só uma vez (evita duplicar
    # quando o modo debug reinicia o processo sozinho).
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        webbrowser.open('http://127.0.0.1:5000/login')

    app.run(debug=True)