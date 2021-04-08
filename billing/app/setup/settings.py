import os

SECRET_KEY = os.environ.get('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask:flask@db/db'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///billing.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
