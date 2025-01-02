#models.py
from datetime import datetime
import pytz

from config import db, ma

class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sql_session = db.session

person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
