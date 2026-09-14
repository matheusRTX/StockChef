from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify

from backend.models.usuario import Usuario
from backend.services.usuario.listar_funcionarios_service import ListarFuncionariosService
from backend.services.usuario.aprovar_funcionario_service import AprovarFuncionarioService
from backend.services.usuario.atualizar_funcionario_service import AtualizarFuncionarioService
from backend.services.usuario.desativar_funcionario_service import DesativarFuncionarioService

usuario_bp = Blueprint('usuario', __name__)


class UsuarioController:
    """Controller responsável pela página e pela API de gestão de
    funcionários do estabelecimento. Todas as rotas são restritas ao
    usuário do tipo Administrador dono do estabelecimento."""

    @staticmethod
    def _funcionario_para_json(funcionario):
        return {
            "id_usuario": funcionario.id_usuario,
            "nome": funcionario.nome,
            "email": funcionario.email,
            "status": funcionario.status,
            "ativo": funcionario.ativo,
        }

    # ---------------------- Guards ----------------------

    @staticmethod
    def exigir_admin_pagina():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'Administrador':
            flash("Acesso restrito ao administrador do estabelecimento.", "danger")
            return redirect(url_for('auth.inicio'))

    @staticmethod
    def exigir_admin_api():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401
        if session.get('user_role') != 'Administrador':
            return jsonify({"erro": "acesso restrito ao administrador do estabelecimento"}), 403

    # ---------------------- Página ----------------------

    @staticmethod
    def pagina():
        guarda = UsuarioController.exigir_admin_pagina()
        if guarda:
            return guarda
        usuario = Usuario.buscar_por_id(session['user_id'])
        return render_template('usuarios.html', usuario=usuario)

    # ---------------------- API ----------------------

    @staticmethod
    def listar():
        funcionarios = ListarFuncionariosService.execute(session['id_estabelecimento'])
        return jsonify([UsuarioController._funcionario_para_json(f) for f in funcionarios])

    @staticmethod
    def aprovar(id_usuario_funcionario):
        try:
            funcionario = AprovarFuncionarioService.execute(
                session['id_estabelecimento'], id_usuario_funcionario
            )
            return jsonify(UsuarioController._funcionario_para_json(funcionario))
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def atualizar(id_usuario_funcionario):
        dados = request.get_json(force=True)
        try:
            funcionario = AtualizarFuncionarioService.execute(
                session['id_estabelecimento'], id_usuario_funcionario, **dados
            )
            return jsonify(UsuarioController._funcionario_para_json(funcionario))
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def inativar(id_usuario_funcionario):
        try:
            DesativarFuncionarioService.execute(
                session['id_estabelecimento'], id_usuario_funcionario
            )
            return jsonify({"mensagem": "Funcionário inativado com sucesso."})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400


# ---------------------- Registro das rotas ----------------------

usuario_bp.add_url_rule('/usuarios', view_func=UsuarioController.pagina, methods=['GET'])

usuario_bp.add_url_rule('/api/usuarios', view_func=UsuarioController.listar, methods=['GET'])
usuario_bp.add_url_rule(
    '/api/usuarios/<int:id_usuario_funcionario>/aprovar',
    view_func=UsuarioController.aprovar, methods=['POST'],
)
usuario_bp.add_url_rule(
    '/api/usuarios/<int:id_usuario_funcionario>',
    view_func=UsuarioController.atualizar, methods=['PUT'],
)
usuario_bp.add_url_rule(
    '/api/usuarios/<int:id_usuario_funcionario>',
    view_func=UsuarioController.inativar, methods=['DELETE'],
)

usuario_bp.before_request(lambda: (
    UsuarioController.exigir_admin_api()
    if request.path.startswith('/api/usuarios') else None
))
