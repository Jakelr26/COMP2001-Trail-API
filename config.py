#config.py
import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import urllib.parse

# database = 'COMP2001_test'
database = 'COMP2001_JLear'
username = 'JLear'
password = 'LekP847*'

encoded_password = urllib.parse.quote_plus(password)

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)
app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mssql+pyodbc://{username}:{encoded_password}@dist-6-505.uopnet.plymouth.ac.uk/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&TrustServerCertificate=yes"
    "&Encrypt=yes"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)



'''app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DIST-6-505.uopnet.plymouth.ac.uk;"
    "DATABASE=COMP2001_JLear;"
    "UID=JLear;"
    "PWD=SkcY333+;"
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
'''
