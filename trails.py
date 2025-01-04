from flask import abort, make_response

from config import db
from models import Trail, Trail_schema, Trail_location_Point, Trail_schemas
from sqlalchemy.orm import joinedload



def read_all():

    trails = Trail.query.all()
    for trail in trails:
        print(trail.Trail_location_point)


    return Trail_schemas.dump(trails)

def read_one(trail_id):
    trail = Trail.query.get(trail_id)

    schema = Trail_schema()
    result = schema.dump(trail)
    if result is None:
        abort(404, f"Trail with id {trail_id} not found")
    return result

def create(trail):
    print(trail)

    if trail is None:
        abort(400, "Request body is missing trail data")

    trail_schema_self = Trail_schema()
    new_trail = trail_schema_self.load(data=trail, session=db.session)
    db.session.add(new_trail)
    db.session.commit()

    schema = Trail_schema()
    result = schema.dump(new_trail)
    return result, 201

def update(trail_id, trail):
    if trail is None:
        abort(400, "Request body is missing trail data")

    existing_trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    if existing_trail:
        trail_schema_self = Trail_schema()
        update_trail = trail_schema_self.load(trail, session=db.session)
        existing_trail.Trail_name = update_trail.Trail_name
        existing_trail.Trail_summary = update_trail.Trail_summary
        existing_trail.Trail_Description = update_trail.Trail_Description
        existing_trail.Difficulty = update_trail.Difficulty
        existing_trail.Location = update_trail.Location
        existing_trail.Distance = update_trail.Distance
        existing_trail.Elevation = update_trail.Elevation
        existing_trail.Route_Type = update_trail.Route_Type
        existing_trail.Owner_ID = update_trail.Owner_ID

        db.session.merge(existing_trail)
        db.session.commit()
        return trail_schema_self.dump(existing_trail), 201
    else:
        abort(404, f"Trail with id {trail_id} not found")

def delete(trail_id):
    existing_trail = Trail.query.filter(Trail.id == trail_id).one_or_none()
    if existing_trail:
        db.session.delete(existing_trail)

