from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel

app = Flask(__name__)
# app.secret_key="@#%$(*&^$%$#@$%&^*%^&*^$%&^*^&*daddfasfcFEDASC"
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:trieu02072002@localhost/it02saledbv2?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app = app)