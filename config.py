import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@DESKTOP-VF9RI0P\SQLEXPRESS/REDWOLFS?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24).hex()
