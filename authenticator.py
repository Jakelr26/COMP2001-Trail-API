import json

import requests
from cryptography.fernet import Fernet
import os
from flask import jsonify, request, Blueprint

from models import User_tabel


#email = 'tim@plymouth.ac.uk'
#pwd = 'COMP2001!'


# function for authorisation
def auth(cred):
    auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users" #link to socem

#Layout of credentails
    # cred ={
    #     'email' : email,
    #     'password' : pwd
    # }

    response = requests.post(auth_url, json=cred) #gets cred


    if response.status_code == 200:
        try:#graceful error handlign
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
SECRET_KEY = "MY_SUPER_DUPER_SECRET_KEY" # my secret key
#(not completely secure as its stored in code, however in scope cant think of better way)

#login response fucntion that encrypts a toke before sening
def login():
    credentials = request.get_json()

    #getting data from JSON input
    pwd = credentials.get("password")
    username = credentials.get("email")

    credentials = { #cred json obj
        'email' : username,
        'password' : pwd
    }

    #Authentication via dle method
    authenticate = auth(credentials) #Uses auth to get a response

    print(authenticate[1]) # debuging print of thei permissions

    if authenticate[1] == 'True' and authenticate[0] == 'Verified': #checks both of the list reponses from auth

        #makes sure they are one of the three provided users
        employees_exist = User_tabel.query.filter(User_tabel.Email == username).one_or_none()
        if employees_exist:
            user_tabel_role = employees_exist.Role
            permToken = {#creates a json object to be the Json token
                "role" : user_tabel_role,
            }
            token = json.dumps(permToken)

            key = Fernet.generate_key() #makes  akey using fernet library from cryptography

            os.environ['key'] = key.decode() #uses os.environ so i dont need a key file (more faff)

            cipher_suite = Fernet(key) #based on what the fernet website says

            permission_token = token
            encrypted_token = cipher_suite.encrypt(permission_token.encode()) #encrypting the token
            print(encrypted_token) # prints the encrypted token

            permissions = {'role_token' : encrypted_token.decode()} #sets a json file of the encrypted token
            with open('permissions.json', 'w') as json_file:
                json.dump(permissions, json_file)
            # print(token)
            # print({'message' : "Login successful"})
            return ('encrytion complete')


            #token in the cookie, was using for the HTML interface
            # response = make_response(redirect(url_for('home')))
            # response.set_cookie('token', token, httponly=True, secure=True) #turn on after development (HTTPS)
            # return response
            # return jsonify({"token" : token}, {"message" : "Login successful"}), 200
    else:
        return jsonify({"message" : "Login failed, Invalid credentials"}), 401 #error check
        #logout()

