from . import db
import datetime
from werkzeug.security import generate_password_hash

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(300))
    email = db.Column(db.String(100))
    location = db.Column(db.String(150))
    biography = db.Column(db.String(500))
    photo = db.Column(db.String(250))
    date_joined = db.Column(db.DateTime, default=datetime.date.today())

    def __init__(self, username, password, name, email, location, biography, photo):
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.name = name
        self.email = email
        self.location = location
        self.biography = biography
        self.photo = photo
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)

class Cars(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    make = db.Column(db.String(250))
    model = db.Column(db.String(300))
    colour = db.Column(db.String(100))
    year = db.Column(db.String(100))
    transmission = db.Column(db.String(300))
    car_type = db.Column(db.String(300))
    price = db.Column(db.Numeric(10,2))
    photo = db.Column(db.String(300))
    user_id = db.Column(db.Integer)

    def __init__(self, user_id, description, make, model, colour, year, transmission, car_type, price, photo):
        self.user_id = user_id
        self.description = description
        self.make = make
        self.model = model
        self.colour = colour
        self.year = year
        self.transmission = transmission
        self.car_type = car_type
        self.price = price
        self.photo = photo
    
    def __repr__(self):
        return '<Car %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r>' % (self.id, self.description, self.make, self.model, self.colour, self.year, self.transmission, self.car_type, self.price, self.photo, self.user_id)

class Favourites(db.Model):
    __tablename__ = 'Favourites'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, user_id, post_id):
        self.car_id = post_id
        self.user_id = user_id

    def __repr__(self):
        return '<Favourite %r>' % (self.id)
