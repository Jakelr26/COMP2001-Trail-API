#app.py
import datetime

import jwt
from flask import render_template, Flask, jsonify, request, session, make_response

from authenticator import auth
import config

from models import Trail, Trail_location_Point
from functools import wraps

app = config.connex_app
app.app.json.sort_keys = False
app.add_api(config.basedir / "swagger.yml")

app.app.config['SECRET_KEY'] = "<MY_SUPER_DUPER_SECRET_KEY>"

def check_for_token(funtion):
    @wraps(funtion)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if token is None:
            return jsonify({'message' : 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403
        return funtion(*args, **kwargs)
    return wrapped

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in as: '

@app.route('/public')
def public():
    return 'Hello, World!'

@app.route("/auth")
@check_for_token
def home():
    trails = Trail.query.all()
    return render_template("home.html", trails=trails)

@app.route("/login", methods=["POST"])
def login():
    pwd = request.form["password"]
    username = request.form["username"]

    authenticate = auth(username, pwd)
    if authenticate:
        session["logged_in"] = True

        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({
            "username" : request.form["username"],
            'expiration' : expiration.timestamp()
        },
        app.app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token" : token})
    else:
        return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

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