import requests, jwt
import datetime

import jwt
from flask import jsonify, request, session, make_response, Blueprint

from config import app
from models import User_tabel


#email = 'tim@plymouth.ac.uk'
#pwd = 'COMP2001!'


login_bp = Blueprint('login', __name__)

def auth(cred):
    auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

    # cred ={
    #     'email' : email,
    #     'password' : pwd
    # }

    response = requests.post(auth_url, json=cred)


    if response.status_code == 200:
        try:
            json_response = response.json()
            print("Authenticated successfully:", json_response)
            return json_response

        except requests.JSONDecodeError:
            print("Response is not valid JSON. Raw response content:")
            print(response.text)

    else:
        print(f"Authentication failed with status code {response.status_code}")
        return 0
    print("Response content:", response.text)


#+@app.route("/login", methods=["POST"])
SECRET_KEY = "MY_SUPER_DUPER_SECRET_KEY"

@login_bp.route("/login", methods=["POST"])
def login():
    credentials = request.get_json()

    pwd = credentials.get("password")
    username = credentials.get("email")

    credentials = {
        'email' : username,
        'password' : pwd
    }

    #Authentication via dle method
    authenticate = auth(credentials)

    print(authenticate[1])

    if authenticate[1] == 'True' and authenticate[0] == 'Verified':

        employees_exist = User_tabel.query.filter(User_tabel.Email == username).one_or_none()
        if employees_exist:
            user_tabel_role = employees_exist.Role
            token = {
                "username" : username,
                "role" : user_tabel_role,
                'expiration' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(token,SECRET_KEY, algorithm="HS256")
            print(token)
            print({'message' : "Login successful"})
            return token


            #token in the cookie, was using for the HTML interface
            # response = make_response(redirect(url_for('home')))
            # response.set_cookie('token', token, httponly=True, secure=True) #turn on after development (HTTPS)
            # return response
            # return jsonify({"token" : token}, {"message" : "Login successful"}), 200
    else:
        return jsonify({"message" : "Login failed, Invalid credentials"}), 401
        #logout()

