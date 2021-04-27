from flask import Flask, request, redirect
import requests
from flask_wtf.csrf import CSRFProtect
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e'
app.config['UPLOAD_FOLDER'] = './app/static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://project2:password123@localhost/project2'
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
