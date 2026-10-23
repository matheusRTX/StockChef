from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify

from backend.models.usuario import Usuario
from backend.services.usuario.autenticar_usuario_service import (
    AutenticarUsuarioService, ContaNaoAprovadaException,
)
from backend.services.usuario.cadastrar_usuario_service import CadastrarUsuarioService
from backend.repositories.inicio_repository import InicioRepository
from backend.services.movimentacao.listar_movimentacoes_service import ListarMovimentacoesService

auth_bp = Blueprint('auth', __name__)


class AuthController:
    """Controller responsável por autenticação, navegação entre páginas e
    pelos endpoints de resumo da tela de início."""

    # ---------------------- Autenticação ----------------------

    @staticmethod
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            senha = request.form.get('senha')

            try:
                usuario = AutenticarUsuarioService.execute(email, senha)
            except ContaNaoAprovadaException as e:
                flash(str(e), "warning")
                return render_template('index.html')

            if usuario:
                session.clear()
                session['user_id'] = usuario.id_usuario
                session['user_name'] = usuario.nome
                session['user_role'] = usuario.tipo

                # id_estabelecimento: chave usada em todo o sistema para
                # escopar os dados (produtos, movimentações, etc.) ao
                # estabelecimento do usuário logado.
                if usuario.tipo == 'Administrador':
                    session['id_estabelecimento'] = usuario.id_usuario
                else:
                    session['id_estabelecimento'] = usuario.id_estabelecimento

                return redirect(url_for('auth.inicio'))
            else:
                flash("E-mail ou senha incorretos.", "danger")

        return render_template('index.html')

    @staticmethod
    def cadastro():
        if request.method == 'POST':
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            tipo = request.form.get('tipo')
            codigo_estabelecimento = request.form.get('codigo_estabelecimento')

            try:
                novo_usuario = CadastrarUsuarioService.execute(
                    nome, email, senha, tipo, codigo_estabelecimento
                )
                if tipo == 'Funcionario':
                    flash(
                        "Cadastro realizado! Sua conta está Pendente e aguardando "
                        "aprovação do administrador do estabelecimento.",
                        "success",
                    )
                else:
                    flash(
                        "Cadastro realizado com sucesso! Seu código de "
                        f"estabelecimento é {novo_usuario.codigo_estabelecimento}. "
                        "Faça o seu login.",
                        "success",
                    )
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash(str(e), "danger")

        return render_template('cadastro.html')

    @staticmethod
    def logout():
        session.clear()
        return redirect(url_for('auth.login'))

    # ---------------------- Navegação (páginas protegidas) ----------------------

    @staticmethod
    def inicio():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        usuario = Usuario.buscar_por_id(session['user_id'])
        return render_template('inicio.html', usuario=usuario)

    @staticmethod
    def cardapio():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return render_template('cardapio.html')

    @staticmethod
    def compras():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return render_template('compras.html')

    @staticmethod
    def pratos():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return render_template('pratos.html')

    @staticmethod
    def qrcode():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return render_template('qrcode.html')

    @staticmethod
    def estoque():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return render_template('estoque.html')

    @staticmethod
    def historico():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return render_template('historico.html')

    # ---------------------- API da tela de início ----------------------

    @staticmethod
    def api_inicio_resumo():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401
        dados = InicioRepository.get_resumo(session['id_estabelecimento'])
        return jsonify(dados)

    @staticmethod
    def api_inicio_estoque_baixo():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401
        dados = InicioRepository.get_estoque_baixo(session['id_estabelecimento'])
        return jsonify(dados)

    @staticmethod
    def api_inicio_vencendo():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401
        dados = InicioRepository.get_vencendo_7_dias(session['id_estabelecimento'])
        return jsonify(dados)

    @staticmethod
    def api_inicio_movimentacoes():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401
        movimentacoes = ListarMovimentacoesService.execute(id_usuario=session['id_estabelecimento'])
        dados = [
            {
                "id_movimentacao": m.id_movimentacao,
                "tipo": m.tipo,
                "data_movimentacao": m.data_movimentacao.isoformat() if m.data_movimentacao else None,
                "observacao": m.observacao,
            }
            for m in movimentacoes[:10]
        ]
        return jsonify(dados)


# ---------------------- Registro das rotas ----------------------

auth_bp.add_url_rule('/', view_func=AuthController.login, methods=['GET'])
auth_bp.add_url_rule('/login', view_func=AuthController.login, methods=['GET', 'POST'])
auth_bp.add_url_rule('/cadastro', view_func=AuthController.cadastro, methods=['GET', 'POST'])
auth_bp.add_url_rule('/logout', view_func=AuthController.logout, methods=['GET'])

auth_bp.add_url_rule('/inicio', view_func=AuthController.inicio, methods=['GET'])
auth_bp.add_url_rule('/cardapio', view_func=AuthController.cardapio, methods=['GET'])
auth_bp.add_url_rule('/compras', view_func=AuthController.compras, methods=['GET'])
auth_bp.add_url_rule('/pratos', view_func=AuthController.pratos, methods=['GET'])
auth_bp.add_url_rule('/qrcode', view_func=AuthController.qrcode, methods=['GET'])
auth_bp.add_url_rule('/estoque', view_func=AuthController.estoque, methods=['GET'])
auth_bp.add_url_rule('/historico', view_func=AuthController.historico, methods=['GET'])

auth_bp.add_url_rule('/api/inicio/resumo', view_func=AuthController.api_inicio_resumo, methods=['GET'])
auth_bp.add_url_rule('/api/inicio/estoque-baixo', view_func=AuthController.api_inicio_estoque_baixo, methods=['GET'])
auth_bp.add_url_rule('/api/inicio/vencendo', view_func=AuthController.api_inicio_vencendo, methods=['GET'])
auth_bp.add_url_rule('/api/inicio/movimentacoes', view_func=AuthController.api_inicio_movimentacoes, methods=['GET'])
