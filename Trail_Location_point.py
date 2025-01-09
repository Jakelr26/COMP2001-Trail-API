from os import abort

from flask import Flask

from config import db
from models import Trail_location_Point, Trail_location_point_schema
from token_checker import role_req

@role_req(
    "User",
    "Administrator")
def read_all():
    Trail_location_points = Trail_location_Point.query.all()
    schema = Trail_location_point_schema(many=True)
    result = schema.dump(Trail_location_points)
    if result is None:
        abort(404, "No trail location points found")
    return result

@role_req(
    "User",
    "Administrator")
def read_one(Trail_location_point_id):
    Trail_location_points = Trail_location_Point.query.get(Trail_location_point_id)
    schema = Trail_location_point_schema()
    result = schema.dump(Trail_location_points)
    if result is None:
        abort(404, f"Trail location point with id {Trail_location_point_id} not found")
    return result

@role_req(
    "Administrator")
def create(Trail_location_point):
    print(Trail_location_point)

    if Trail_location_point is None:
        abort(400, "Request body is missing trail location point data")

    Trail_location_point_schema_self = Trail_location_point_schema()
    new_Trail_location_point = Trail_location_point_schema_self.load(data=Trail_location_point, session=db.session)
    db.session.add(new_Trail_location_point)
    db.session.commit()

    schema = Trail_location_point_schema()
    result = schema.dump(new_Trail_location_point)
    return result, 201

@role_req(
    "Administrator")
def update(Trail_location_point_id, Trail_location_point):
    if Trail_location_point is None:
        abort(400, "Request body is missing trail location point data")

    existing_Trail_location_point = Trail_location_point.query.filter(Trail_location_point.Trail_location_point_id == Trail_location_point_id).one_or_none()
    if existing_Trail_location_point:
        Trail_location_point_schema_self = Trail_location_point_schema()
        update_Trail_location_point = Trail_location_point_schema_self.load(Trail_location_point, session=db.session)

        existing_Trail_location_point.Trail_location_point_id = update_Trail_location_point.Trail_location_point_id
        existing_Trail_location_point.Trail_ID = update_Trail_location_point.Trail_ID
        existing_Trail_location_point.Location_Point_ID = update_Trail_location_point.Location_Point_ID

        db.session.merge(existing_Trail_location_point)
        db.session.commit()
        return Trail_location_point_schema_self.dump(existing_Trail_location_point), 201
    else:
        abort(404, f"Trail location point with id {Trail_location_point_id} not found")

@role_req(
    "Administrator"
)
def delete(Trail_location_point_id):
    existing_Trail_location_point = Trail_location_Point.query.filter(Trail_location_Point.id == Trail_location_point_id).one_or_none()
    if existing_Trail_location_point:
        db.session.delete(existing_Trail_location_point)