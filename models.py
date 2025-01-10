#models.py

from sqlalchemy.orm import relationship
from marshmallow import fields

from config import db, ma


# LocationPoint model
class LocationPoint(db.Model):
    __tablename__ = "LocationPoint"
    __table_args__ = {'schema': 'cw2'}  # Specify the schema

    Location_Point = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)


class LocationPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True
        sqla_session = db.session
        ordered = True

        #exclude = ["Location_Point"]

    latitude = fields.Float()
    longitude = fields.Float()
    description = fields.Str()


# Trail_location_point model
class Trail_location_Point(db.Model):
    __tablename__ = "Trail_location_Point"
    __table_args__ = {'schema': 'cw2'}  # Specify the schema

    Trail_ID = db.Column(
        db.Integer,
        db.ForeignKey("cw2.Trail.Trail_ID"),
        primary_key=True,
        nullable=False)
    Location_Point = db.Column(
        db.Integer,
        db.ForeignKey(
            "cw2.LocationPoint.Location_Point",
            ondelete="CASCADE"
        ),
        nullable=False,
        primary_key=True)
    Order_no = db.Column(db.Integer, nullable=False)

    LocationPoint = relationship("LocationPoint",
         backref=db.backref(
             "Trail_location_point",
             cascade="all, delete, delete-orphan",
             passive_deletes=True
         )
     )


class Trail_location_Point_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail_location_Point
        load_instance = True
        sqla_session = db.session
        #include_fk = True
        include_relationships = True
        ordered = True

        exclude = ("Trail_ID", "Location_Point")

    Order_no = fields.Integer()

    LocationPoint = fields.Nested(LocationPointSchema)


# Feature model
class Feature(db.Model):
    __tablename__ = "Feature"
    __table_args__ = {'schema': 'cw2'}  # Specify the schema

    trail_feature_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    trail_feature = db.Column(
        db.String,
        nullable=True
    )


class Feature_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sqla_session = db.session
        ordered = True

    trail_feature = fields.Str()


# Trail_feature model
class Trail_feature(db.Model):
    __tablename__ = "Trail_Feature"
    __table_args__ = {'schema': 'cw2'}  # Specify the schema

    Trail_ID = db.Column(
        db.Integer,
        db.ForeignKey("cw2.Trail.Trail_ID"),
        primary_key=True,
        nullable=False
    )
    Trail_Feature_ID = db.Column(
        db.Integer,
        db.ForeignKey("cw2.Feature.trail_feature_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    Feature = db.relationship(
        "Feature",
        backref=db.backref(
            "Trail_feature",
            cascade="all, delete, delete-orphan",
            passive_deletes=True
        )
    )


class Trail_feature_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail_feature
        load_instance = True
        sqla_session = db.session
        include_fk = True
        ordered = True


# User_tabel model
class User_tabel(db.Model):
    __tablename__ = "user_tabel"
    __table_args__ = {'schema': 'cw2'}  # Specify the schema

    User_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Email = db.Column(db.String, nullable=False)
    Role = db.Column(db.String, nullable=False)


class User_tabel_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User_tabel
        load_instance = True
        sqla_session = db.session
        ordered = True


# Trail model
class Trail(db.Model):
    __tablename__ = "Trail"
    __table_args__ = {'schema': 'cw2'}  # Specify the schema

    Trail_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Trail_name = db.Column(db.String, nullable=False)
    Trail_summary = db.Column(db.String, nullable=True)
    Trail_Description = db.Column(db.String, nullable=True)
    Difficulty = db.Column(db.String, nullable=True)
    Location = db.Column(db.String, nullable=True)
    Distance = db.Column(db.Integer, nullable=False)
    Elevation = db.Column(db.Integer, nullable=False)
    Route_Type = db.Column(db.String, nullable=True)
    Owner_ID = db.Column(
        db.Integer,
        db.ForeignKey("cw2.user_tabel.User_id"),
        nullable=False
    )

    Trail_location_point = db.relationship(
        Trail_location_Point,
        backref="Trail",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by=Trail_location_Point.Order_no
        #lazy="joined"
    )

    Trail_feature = db.relationship(
        Trail_feature,
        backref="Trail",
        cascade="all, delete, delete-orphan",
    )


class Trailschema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        ordered = True
        load_instance = True
        sqla_session = db.session
        include_fk = True
        include_relationships = True

    Trail_ID = fields.Integer()
    Trail_name = fields.Str()
    Trail_summary = fields.Str()
    Trail_Description = fields.Str()
    Difficulty = fields.Str()
    Location = fields.Str()
    Distance = fields.Integer()
    Elevation = fields.Integer()
    Route_Type = fields.Str()
    Owner_ID = fields.Integer()
    Trail_location_point = fields.Nested(Trail_location_Point_schema, many=True)
    Trail_feature = fields.Nested(Trail_feature_schema, many=True)



LocationPoint_schema = LocationPointSchema()
LocationPoint_schemas = LocationPointSchema(many=True)

Trail_location_point_schema = Trail_location_Point_schema()

'''
class Note(db.Model):
    __tablename__ = "note"
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )
    notes = db.relationship(
        'Note',
        backref="person",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    notes = fields.Nested(NoteSchema, many = True)

person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
'''
