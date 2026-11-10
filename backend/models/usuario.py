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

    codigo_estabelecimento = db.Column(db.String(10), unique=True, nullable=True)

    id_estabelecimento = db.Column(
        db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True
    )

    status = db.Column(
        db.Enum('Pendente', 'Aprovado', 'Recusado'),
        nullable=False,
        default='Aprovado',
    )

    camera_autorizada = db.Column(
        db.Boolean, nullable=False, default=False, server_default=db.text('0')
    )

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
        usuario.ativo = False
        db.session.commit()
