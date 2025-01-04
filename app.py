#app.py

from flask import render_template, Flask
import config
from models import Trail

from models import Trail, Trail_location_Point


app = config.connex_app

app.app.json.sort_keys = False

app.add_api(config.basedir / "swagger.yml")



@app.route("/")
def home():
    trails = Trail.query.all()
    return render_template("home.html", trails=trails)
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
'''