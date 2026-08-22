import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/stockchef'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24) 

# casa:
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Bio780412@127.0.0.1:3306/stockchef'

# escola:
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/stockchef'