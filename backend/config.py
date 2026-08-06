import os

class Config:
    # Atualizado com o usuário root e a sua nova senha Bio780412
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Bio780412@127.0.0.1:3306/stockchef'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)