from flask import Flask, request, redirect
import requests
from flask_wtf.csrf import CSRFProtect
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e'
app.config['UPLOAD_FOLDER'] = './app/static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xfkfcbbpdmtlvl:d9b7d00946507e9afc9a4fc0a949c8b3e95f491fe3c3a359f5b3688408f8a05b@ec2-107-20-153-39.compute-1.amazonaws.com:5432/d8sb0lkluhhssr'
HEROKU_POSTGRESQL_COPPER_URL='postgres://nnrgwpacawumhp:e541a82dd4eebc75fadb639602ecfab5e039a6530503bf6a870dabd95b4ea737@ec2-107-20-153-39.compute-1.amazonaws.com:5432/d95d2efrttk5qn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SALT'] = 'r?fPfnryZfJ=M*aQxz$h2_F#!X@YR9nEB&f^SU3qRkVTt3WeP528BRYGthRZ7@8hT4Wqh'

db = SQLAlchemy(app)

WTF_CSRF_ENABLED = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

csrf = CSRFProtect(app)
csrf.init_app(app)

app.config.from_object(__name__)

from app import views, models, forms
