import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Bio780412@localhost:3306/stockchef'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AQ.Ab8RN6LVEqh2pi7MII2p3Vwqh0MJ1epfIG3DS-3TQCVptFXzGg')


# escola:
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/stockchef'