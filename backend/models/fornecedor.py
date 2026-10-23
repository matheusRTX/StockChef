from backend.models.usuario import db


class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'

    id_fornecedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(25))
    email = db.Column(db.String(150))
    endereco = db.Column(db.String(255))
    contato = db.Column(db.String(100))
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    observacao = db.Column(db.Text)

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(id_usuario, nome, telefone=None, email=None, endereco=None, contato=None, observacao=None):
        novo = Fornecedor(
            id_usuario=id_usuario,
            nome=nome,
            telefone=telefone,
            email=email,
            endereco=endereco,
            contato=contato,
            observacao=observacao,
        )
        db.session.add(novo)
        db.session.commit()
        return novo

    @staticmethod
    def buscar_por_id(id_fornecedor):
        return Fornecedor.query.get(id_fornecedor)

    @staticmethod
    def listar_por_usuario(id_usuario):
        return (
            Fornecedor.query
            .filter_by(id_usuario=id_usuario, ativo=True)
            .order_by(Fornecedor.nome)
            .all()
        )

    @staticmethod
    def atualizar(fornecedor, **campos):
        campos_validos = {'nome', 'telefone', 'email', 'endereco', 'contato', 'observacao'}
        for campo, valor in campos.items():
            if campo in campos_validos:
                setattr(fornecedor, campo, valor)
        db.session.commit()
        return fornecedor

    @staticmethod
    def deletar(fornecedor):
        # remove primeiro o vínculo com a tabela associativa fornecedor_categoria
        db.session.execute(
            db.text('DELETE FROM fornecedor_categoria WHERE id_fornecedor = :id_fornecedor'),
            {'id_fornecedor': fornecedor.id_fornecedor},
        )
        db.session.delete(fornecedor)
        db.session.commit()

    # ---------------------- Categoria (tabela fornecedor_categoria) ----------------------
    # A tabela fornecedores não guarda a categoria diretamente: ela é ligada por meio
    # da tabela associativa fornecedor_categoria (permite N categorias, mas o
    # formulário atual só permite escolher uma por fornecedor).

    @staticmethod
    def definir_categoria(id_fornecedor, id_categoria):
        db.session.execute(
            db.text('DELETE FROM fornecedor_categoria WHERE id_fornecedor = :id_fornecedor'),
            {'id_fornecedor': id_fornecedor},
        )
        if id_categoria:
            db.session.execute(
                db.text(
                    'INSERT INTO fornecedor_categoria (id_fornecedor, id_categoria) '
                    'VALUES (:id_fornecedor, :id_categoria)'
                ),
                {'id_fornecedor': id_fornecedor, 'id_categoria': id_categoria},
            )
        db.session.commit()

    @staticmethod
    def buscar_categoria(id_fornecedor):
        linha = db.session.execute(
            db.text(
                'SELECT c.id_categoria, c.nome '
                'FROM fornecedor_categoria fc '
                'INNER JOIN categorias c ON c.id_categoria = fc.id_categoria '
                'WHERE fc.id_fornecedor = :id_fornecedor '
                'LIMIT 1'
            ),
            {'id_fornecedor': id_fornecedor},
        ).first()
        if not linha:
            return None
        return {'id_categoria': linha[0], 'nome': linha[1]}
