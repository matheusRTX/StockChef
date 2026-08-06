from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = AuthService.login_usuario(email, senha)
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
            AuthService.cadastrar_usuario(nome, email, senha, tipo)
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

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))