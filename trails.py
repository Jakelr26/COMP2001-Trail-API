from flask import abort, make_response

from config import db
from models import Trail, Trailschema, Trail_location_Point
from sqlalchemy.orm import joinedload

from token_checker import role_req


@role_req("User", "Administrator")
def read_all():

    trails = Trail.query.all()
    for trail in trails:
        print(trail.Trail_location_point)

    schema = Trailschema(many=True)

    return schema.dump(trails)
@role_req(
    "User",
    "Administrator")
def read_one(trail_id):
    trail = Trail.query.get(trail_id)

    schema = Trailschema()
    result = schema.dump(trail)
    if result is None:
        abort(404, f"Trail with id {trail_id} not found")
    return result

@role_req("Administrator")
def create(trail):
    print(trail)

    if trail is None:
        abort(400, "Request body is missing trail data")

    trail_schema_self = Trailschema()
    new_trail = trail_schema_self.load(data=trail, session=db.session)
    db.session.add(new_trail)
    db.session.commit()


    result = Trailschema().dump(new_trail)
    return result, 201

@role_req("Administrator")
def update(trail_id, trail):
    if trail is None:
        abort(400, "Request body is missing trail data")

    existing_trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    if existing_trail:
        trail_schema_self = Trailschema()
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

@role_req
def delete(trail_id):
    print(f"delete() invoked with: {trail_id}")
    existing_trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    if existing_trail:
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"{trail_id} successfully deleted", 200)

