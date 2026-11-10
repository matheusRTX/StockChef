import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Bio780412@localhost:3306/stockchef'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AQ.Ab8RN6K4TNSNukTvB5hc9W2YPm-sPrHw6StAdMZ64Q4p3egoYw')

