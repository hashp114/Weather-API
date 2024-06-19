import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/code_challenge_template')
    SQLALCHEMY_TRACK_MODIFICATIONS = False