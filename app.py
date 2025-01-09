#app.py
import datetime

import jwt
from flask import render_template, Flask, jsonify, request, session, make_response, redirect, url_for

from authenticator import auth
import config

from models import Trail, Trail_location_Point
from functools import wraps

app = config.connex_app
app.app.json.sort_keys = False
app.add_api(config.basedir / "./")
#

app.app.config['SECRET_KEY'] = "<MY_SUPER_DUPER_SECRET_KEY>"

def check_for_token(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        token = request.cookies.get('token') #get token from login

        if token is None:
            return jsonify({'message' : 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message' : 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return function(*args, **kwargs)
    return wrapped

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        username = session.get('username')
        if username:
            return 'Logged in as: '.format(session['username'])
        else:
            return 'Logged in, but username is missing from the session!'

@app.route('/public')
def public():
    return 'Hello, World!'

@app.route("/auth", methods=["GET"])
@check_for_token
def home():
    trails = Trail.query.all()

    return redirect("/api/ui/")
    #return render_template("home.html", trails=trails)

@app.route("/api/ui/")
@check_for_token
def the_swag():
    return redirect("/api/ui")

@app.app.before_request
def protect_the_swag():
    if '/api/ui/' in request.path:
        token = request.cookies.get('token')
        if token is None:
            return jsonify({'message' : 'Token is missing! So you dont have permissions to be here'}), 403
        try:
            data = jwt.decode(token, app.app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message' : 'Session has finished, re-login or finish!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message' : 'Token is invalid! So you dont have permissions to be here :('}), 403

@app.app.before_request
def protect_the_swag_endpoints():
    if '/api/ui/' in request.path:
        token = request.cookies.get('token')
        if token is None:
            return jsonify({'message' : 'Token is missing! So you dont have permissions to be here :('}), 403
        try:
            data = jwt.decode(token, app.app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message' : 'Session has finished, re-login or finish!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message' : 'Token is invalid! So you dont have permissions to be here :('}), 403


@app.route("/login", methods=["POST"])
def login():
    pwd = request.form["password"]
    username = request.form["username"]

    print(pwd)
    print(username)

    credentials = {
        'email' : username,
        'password' : pwd
    }

    #Authentication via dle method
    authenticate = auth(credentials)

    print(authenticate)

    if authenticate == ['Verified', 'True']:
        session["logged_in"] = True
        session["username"] = username

        expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        token = jwt.encode({
            "username" : username,
            'expiration' : expiration.timestamp()},
            app.app.config['SECRET_KEY'], algorithm="HS256"
        )

        #token in the cookie
        response = make_response(redirect(url_for('home')))
        response.set_cookie('token', token, httponly=True, secure=True) #turn on after development (HTTPS)
        return response
    else:
        #logout()
        return render_template('login.html', error="Invalid username or password. Please try again."), 401

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()

    response = make_response(jsonify({"message" : "Logout successful"}), 200)
    response.set_cookie('token', '', expires=0)

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


'''
from models import Person

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    people = Person.query.all()
    return render_template("home.html", people=people)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    
    DB is back fo business
    
'''