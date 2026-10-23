from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum('Administrador', 'Funcionario'), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    # ---------------------- Multi-tenant / vínculo com estabelecimento ----------------------

    # Preenchido apenas para usuários do tipo Administrador: código único que
    # identifica o estabelecimento dele e é usado pelo Funcionário no cadastro.
    codigo_estabelecimento = db.Column(db.String(10), unique=True, nullable=True)

    # Preenchido apenas para usuários do tipo Funcionario: aponta para o
    # id_usuario do Administrador dono do estabelecimento ao qual ele
    # está vinculado (auto-relacionamento na própria tabela usuarios).
    id_estabelecimento = db.Column(
        db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True
    )

    # Situação do cadastro. Administrador nasce sempre 'Aprovado'.
    # Funcionario nasce 'Pendente' e só pode operar no sistema após o
    # Administrador do estabelecimento aprová-lo.
    status = db.Column(
        db.Enum('Pendente', 'Aprovado', 'Recusado'),
        nullable=False,
        default='Aprovado',
    )

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(nome, email, senha_hash, tipo, codigo_estabelecimento=None,
              id_estabelecimento=None, status='Aprovado'):
        novo = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash,
            tipo=tipo,
            codigo_estabelecimento=codigo_estabelecimento,
            id_estabelecimento=id_estabelecimento,
            status=status,
        )
        db.session.add(novo)
        db.session.commit()
        return novo

    @staticmethod
    def buscar_por_id(id_usuario):
        return Usuario.query.get(id_usuario)

    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def buscar_por_codigo_estabelecimento(codigo_estabelecimento):
        return Usuario.query.filter_by(
            codigo_estabelecimento=codigo_estabelecimento,
            tipo='Administrador',
        ).first()

    @staticmethod
    def listar_todos():
        return Usuario.query.filter_by(ativo=True).all()

    @staticmethod
    def listar_funcionarios_do_estabelecimento(id_estabelecimento):
        """Lista todos os funcionários (qualquer status) vinculados ao
        estabelecimento de um Administrador, do mais recente para o mais antigo."""
        return (
            Usuario.query
            .filter_by(tipo='Funcionario', id_estabelecimento=id_estabelecimento)
            .order_by(Usuario.status.asc(), Usuario.nome.asc())
            .all()
        )

    @staticmethod
    def atualizar(usuario, **campos):
        for campo, valor in campos.items():
            setattr(usuario, campo, valor)
        db.session.commit()
        return usuario

    @staticmethod
    def deletar(usuario):
        # Soft delete: mantém o registro, apenas desativa
        usuario.ativo = False
        db.session.commit()
