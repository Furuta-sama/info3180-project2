"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, login_manager
from flask import render_template, request, jsonify, session, g
from flask_login import login_user, logout_user, current_user, login_required
from .forms import UserForm, LoginForm, CarForm
from app.models import Users, Cars, Favourites
from . import db
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from flask import send_from_directory
import os
import uuid
import hashlib

# Using JWT
import jwt
from flask import _request_ctx_stack
from functools import wraps
import base64

# Create a JWT @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token, app.config['SALT'])

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated


###
# Routing for your application.
###

@app.route('/api/register', methods=['POST'])
def register():
    user = UserForm()
    message = [{"errors": "critical error"}]
    if request.method == 'POST':
        user.username.data = request.form['username']
        user.password.data = request.form['password']
        user.name.data = request.form['name']
        user.email.data = request.form['email']
        user.location.data = request.form['location']
        user.biography.data = request.form['biography']
        user.photo.data = request.files['photo']
        message = [{"errors": form_errors(user)}]
        if user.validate_on_submit():
            username = user.username.data
            password = user.password.data
            name = user.name.data
            email = user.email.data
            location = user.location.data
            biography = user.biography.data
            photo = user.photo.data

            filename = genUniqueFileName(photo.filename)
            userDB = Users(username, password, name, email, location, biography, filename)
            db.session.add(userDB)
            db.session.commit()
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            message = [{"message": "Successful Registered!"}]

    message = jsonify(message=message)
    return message

@app.route('/api/auth/login', methods=['POST'])
def login():
    form = LoginForm()
    message = [{"errors": "Invalid request"}]
    if request.method == "POST":
        form.username.data = request.form['username']
        form.password.data = request.form['password']
        message = [{"errors": form_errors(form)}]

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = Users.query.filter_by(username=username).first()

            if user is not None and check_password_hash(user.password, password):

                payload = {'id': user.id, 'username': user.username}
                token = jwt.encode(payload, app.config['SALT'], algorithm='HS256').decode('utf-8')

                return jsonify(data={'token': token}, message="Token Generated and User Logged In")
            else:
                message = [{"errors": "Failed to Log In"}]
    message = jsonify(message=message)
    return message

#@login_required
@app.route('/api/auth/logout', methods=['GET'])
@requires_auth
def logout():
    #logout_user()
    #complete
    #session['user_id'] = None
    user = g.current_user
    return jsonify(data={"user": user}, message="Logged Out")

@app.route('/api/cars', methods=['GET', 'POST'])
@requires_auth
def cars():
    message = [{"errors": "Invalid request"}]
    if request.method == "GET":
        cars = Cars.query.order_by(Cars.id).all()
        allcars = []
        for c in cars:
            car = {}
            car['id'] = c.id
            car['description'] = c.description
            car['year'] = c.year
            car['make'] = c.make
            car['colour'] = c.colour
            car['model'] = c.model
            car['transmission'] = c.transmission
            car['car_type'] = c.car_type
            car['price'] = float(c.price)
            car['photo'] = c.photo
            car['user_id'] = c.user_id
            allcars+= [car]
        return jsonify(allcars)
    elif request.method == "POST":
        car = CarForm()
        message = [{"errors": form_errors(car)}]
        if car.validate_on_submit():
            print("Hi mom") 
            desc = car.description.data
            make = car.make.data
            model = car.model.data
            colour = car.colour.data
            year = car.year.data
            transmission = car.transmission.data
            car_type = car.car_type.data
            price = car.price.data
            photo = car.photo.data
            user = g.current_user
            user_id = user["id"]

            filename = secure_filename(photo.filename)
            photo.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            ))

            carDB = Cars(user_id, desc, make, model, colour, year, transmission, car_type, price, filename)
            db.session.add(carDB)
            db.session.commit()

            message = [{"message": "Successful Posted!"}]
    message = jsonify(message=message)
    return message

@app.route('/api/cars/<car_id>', methods=['GET'])
@requires_auth
def get_car(car_id):
    c = Cars.query.filter_by(id=car_id).first()
    car = {}
    car['id'] = c.id
    car['description'] = c.description
    car['year'] = c.year
    car['make'] = c.make
    car['colour'] = c.colour
    car['model'] = c.model
    car['transmission'] = c.transmission
    car['car_type'] = c.car_type
    car['price'] = float(c.price)
    car['photo'] = c.photo
    car['user_id'] = c.user_id
    return jsonify(car)

@app.route('/api/cars/<car_id>/favourite', methods=['POST'])
@requires_auth
def add_fav(car_id):
    message = [{"errors": "Invalid request"}]
    if request.method == 'POST':
            fav = Favourites(car_id, g.current_user['id'])
            db.session.add(fav)
            db.session.commit()
            message = [{"message": "Car Successfully Favourited", "car_id": car_id}]
    return jsonify(message)

#@app.route('/api/search/')

@app.route('/api/users/<user_id>', methods=['GET'])
@requires_auth
def get_user(user_id):
    message = [{"errors": "Invalid request"}]
    if request.method == 'GET':
        u = Users.query.filter_by(id=user_id).first()
        user = {}
        user['id'] = u.id
        user['username'] = u.username
        user['name'] = u.name
        user['photo'] = u.photo
        user['email'] = u.email
        user['location'] = u.location
        user['biography'] = u.biography
        user['date_joined'] = u.date_joined
        return jsonify(user)
    return jsonify(message)

@app.route('/api/users/<user_id>/favourites', methods=['GET'])
@requires_auth
def get_favs(user_id):
    message = [{"errors": "Invalid request"}]
    if request.method == 'GET':
        favs = Favourites.query.filter_by(id=user_id).all()
        allfavs = []
        for f in favs:
            fav = {}
            fav['car_id'] = f.car_id
            fav['user_id'] = f.user_id
            allfavs+= [fav] 
        return jsonify(allfavs)
    return jsonify(message)

@app.route('/api/secure', methods=['GET'])
@requires_auth
def api_secure():
    # This data was retrieved from the payload of the JSON Web Token
    # take a look at the requires_auth decorator code to see how we decoded
    # the information from the JWT.
    user = g.current_user
    return jsonify(data={"user": user}, message="Success")

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.route("/static/uploads/<path:filename>")
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

# Please create all new routes and view functions above this route.
# This route is now our catch all route for our VueJS single page
# application.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".

    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('index.html')


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


###
# The functions below should be applicable to all Flask apps.
###

def genUniqueFileName(old_filename):
    filename = str(uuid.uuid4())
    ext = old_filename.split(".")
    ext = ext[1]
    new_filename = filename + "." + ext
    new_filename = new_filename.replace('-', '_')
    return new_filename

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
