#app.py
from flask import render_template, jsonify, session, make_response

import config
from models import Trail


app = config.connex_app
app.app.json.sort_keys = False
app.add_api(config.basedir / "swagger.yml")

#the secret key, no very secure as in the code, but due to scope is the only option i can think of
app.app.config['SECRET_KEY'] = "MY_SUPER_DUPER_SECRET_KEY"

#the home page endpoint "/"
@app.route("/")
def home():
    trails = Trail.query.all()

    #return redirect("/api/ui/")
    return render_template("home.html", trails=trails) # renders home.html

#logout endpoint that ends the session
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()

    response = make_response(jsonify({"message" : "Logout successful"}), 200)
    response.set_cookie('token', '', expires=0)

    return response

#used to run the whole of app.py
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