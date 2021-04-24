from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    name = StringField('firstname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])
    biography = TextAreaField('biography', validators=[DataRequired()])
    photo = FileField('photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'Images only!'])
    ])

class CarForm(FlaskForm):
    description = StringField('description', validators=[DataRequired()])
    make = StringField('make', validators=[DataRequired()])
    model = StringField('model', validators=[DataRequired()])
    color = StringField('color', validators=[DataRequired()])
    year = StringField('year', validators=[DataRequired()])
    transmission = StringField('location', validators=[DataRequired()])
    car_type = StringField('car_type', validators=[DataRequired()])
    price = DecimalField('price', validators=[DataRequired()])
    photo = FileField('photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'Images only!'])
    ])

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class PostForm(FlaskForm):
    photo = FileField('photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'Images only!'])])
    caption = TextAreaField('caption', validators=[DataRequired()])

class LikeForm(FlaskForm):
    userid = IntegerField('userid', validators=[DataRequired()])

class FollowForm(FlaskForm):
    following = IntegerField('following', validators=[DataRequired()])