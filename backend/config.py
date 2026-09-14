import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/stockchef'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24) 


# escola:
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/stockchef'