#app.py
import datetime

import jwt
from flask import render_template, Flask, jsonify, request, session, make_response, redirect, url_for

from authenticator import auth
import config
from models import Trail, Trail_location_Point
from functools import wraps

from token_checker import role_req

app = config.connex_app
app.app.json.sort_keys = False
app.add_api(config.basedir / "swagger.yml")

app.app.config['SECRET_KEY'] = "MY_SUPER_DUPER_SECRET_KEY"


@app.route("/")
def home():
    trails = Trail.query.all()

    #return redirect("/api/ui/")
    return render_template("home.html", trails=trails)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()

    response = make_response(jsonify({"message" : "Logout successful"}), 200)
    response.set_cookie('token', '', expires=0)

    return response


if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
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