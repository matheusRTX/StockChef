from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from backend.services.usuario.autenticar_usuario_service import AutenticarUsuarioService
from backend.services.usuario.cadastrar_usuario_service import CadastrarUsuarioService
from backend.repositories.inicio_repository import InicioRepository
from backend.services.movimentacao.listar_movimentacoes_service import ListarMovimentacoesService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = AutenticarUsuarioService.execute(email, senha)
        if usuario:
            session['user_id'] = usuario.id_usuario
            session['user_name'] = usuario.nome
            session['user_role'] = usuario.tipo
            return redirect(url_for('auth.inicio'))
        else:
            flash("E-mail ou senha incorretos.", "danger")

    return render_template('index.html')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')

        try:
            CadastrarUsuarioService.execute(nome, email, senha, tipo)
            flash("Cadastro realizado com sucesso! Faça o seu login.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(str(e), "danger")

    return render_template('cadastro.html')

@auth_bp.route('/inicio')
def inicio():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('inicio.html')

@auth_bp.route('/api/inicio/resumo')
def api_inicio_resumo():
    if 'user_id' not in session:
        return jsonify({"erro": "não autenticado"}), 401
    dados = InicioRepository.get_resumo(session['user_id'])
    return jsonify(dados)

@auth_bp.route('/api/inicio/estoque-baixo')
def api_inicio_estoque_baixo():
    if 'user_id' not in session:
        return jsonify({"erro": "não autenticado"}), 401
    dados = InicioRepository.get_estoque_baixo(session['user_id'])
    return jsonify(dados)

@auth_bp.route('/api/inicio/vencendo')
def api_inicio_vencendo():
    if 'user_id' not in session:
        return jsonify({"erro": "não autenticado"}), 401
    dados = InicioRepository.get_vencendo_7_dias(session['user_id'])
    return jsonify(dados)

@auth_bp.route('/api/inicio/movimentacoes')
def api_inicio_movimentacoes():
    if 'user_id' not in session:
        return jsonify({"erro": "não autenticado"}), 401
    movimentacoes = ListarMovimentacoesService.execute(id_usuario=session['user_id'])
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

@auth_bp.route('/cardapio')
def cardapio():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('cardapio.html')

@auth_bp.route('/compras')
def compras():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('compras.html')

@auth_bp.route('/pratos')
def pratos():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('pratos.html')

@auth_bp.route('/qrcode')
def qrcode():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('qrcode.html')

@auth_bp.route('/estoque')
def estoque():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('estoque.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
