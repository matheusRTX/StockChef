import os
import webbrowser
from flask import Flask
from backend.config import Config

# ---------------------- Models ----------------------
# Importar todos os Models aqui é necessário para que o db.create_all()
# consiga enxergar e criar todas as tabelas do sistema.
from backend.models.usuario import db
from backend.models.categoria import Categoria
from backend.models.unidade_medida import UnidadeMedida
from backend.models.produto import Produto
from backend.models.lote import Lote
from backend.models.movimentacao import Movimentacao
from backend.models.movimentacao_item import MovimentacaoItem
from backend.models.movimentacao_lote import MovimentacaoLote
from backend.models.tipo_culinaria import TipoCulinaria
from backend.models.prato import Prato
from backend.models.prato_ingrediente import PratoIngrediente

# ---------------------- Controllers (Blueprints) ----------------------
from backend.controllers.auth_controller import auth_bp
from backend.controllers.categoria_controller import categoria_bp
from backend.controllers.unidade_medida_controller import unidade_medida_bp
from backend.controllers.produto_controller import produto_bp
from backend.controllers.lote_controller import lote_bp
from backend.controllers.movimentacao_controller import movimentacao_bp
from backend.controllers.tipo_culinaria_controller import tipo_culinaria_bp
from backend.controllers.prato_controller import prato_bp
from backend.controllers.estoque_controller import estoque_api_bp

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

# Registra as rotas de todas as Controllers
app.register_blueprint(auth_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(unidade_medida_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(lote_bp)
app.register_blueprint(movimentacao_bp)
app.register_blueprint(tipo_culinaria_bp)
app.register_blueprint(prato_bp)
app.register_blueprint(estoque_api_bp)

if __name__ == '__main__':
    # Cria as tabelas se elas não existirem (não apaga os dados existentes)
    with app.app_context():
        db.create_all()

    # Abre o navegador automaticamente, só uma vez (evita duplicar
    # quando o modo debug reinicia o processo sozinho).
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        webbrowser.open('http://127.0.0.1:5000/login')

    app.run(debug=True)


    # flask_sqlalchemy, pymysql e werkzeug
