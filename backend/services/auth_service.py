from backend.models.usuario import Usuario, db
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    
    @staticmethod
    def cadastrar_usuario(nome, email, senha, tipo):
        # Verifica se o e-mail já existe no banco
        if Usuario.query.filter_by(email=email).first():
            raise Exception("Este e-mail já está cadastrado no StockChef.")
        
        # Cria o hash seguro da senha
        senha_hash = generate_password_hash(senha)
        
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash,
            tipo=tipo
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario

    @staticmethod
    def login_usuario(email, senha):
        usuario = Usuario.query.filter_by(email=email, ativo=True).first()
        
        # Compara a senha digitada com o hash salvo no banco
        if usuario and check_password_hash(usuario.senha, senha):
            return usuario
        return None