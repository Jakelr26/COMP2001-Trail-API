from flask import abort, make_response

from config import db
from models import LocationPoint, LocationPointSchema, Trail, Trail_location_Point, Trail_schema
from sqlalchemy.orm import joinedload

def read_all():
    '''locationPoints = LocationPoint.query.all()
    schema = LocationPointSchema(many=True)
    result = schema.dump(locationPoints)'''
    trails = Trail.query.options(
        joinedload(Trail.Trail_location_point).joinedload(Trail_location_Point.location_point_obj)
    ).all()

    schema = Trail_schema(many=True)
    result = schema.dump(trails)

    if result is None:
        abort(404, "No location points found")
    return result

def read_one(locationPoint_id):
    locationPoint = LocationPoint.query.get(locationPoint_id)
    schema = LocationPointSchema()
    result = schema.dump(locationPoint)
    if result is None:
        abort(404, f"Location point with id {locationPoint_id} not found")
    return result

def create(locationPoint):
    print(locationPoint)

    if locationPoint is None:
        abort(400, "Request body is missing location point data")
    if "latitude" not in locationPoint or "longitude" not in locationPoint:
        abort(400, "Missing required fields: latitude, longitude")

    locationPoint_tabele_only = {
        "latitude": locationPoint["latitude"],
        "longitude": locationPoint["longitude"],
        "description": locationPoint.get("description")
    }

    locationPoint_schema_self = LocationPointSchema()
    new_locationPoint = locationPoint_schema_self.load(data=locationPoint_tabele_only, session=db.session)
    db.session.add(new_locationPoint)
    db.session.commit()

    trail_id = locationPoint.get("Trail_ID")
    if not trail_id:
        trail = Trail.query.get(trail_id)
        if not trail:
            abort(404, f"Trail with id {trail_id} not found")

        abort(400, "Missing required field: Trail_ID")

    order_no = locationPoint.get("Order_no", 0)

    #no dupe ordernumn
    duplicate_order_no = Trail_location_Point.query.filter_by(Trail_ID=trail_id, Order_no=order_no).one_or_none()
    if duplicate_order_no:
        abort(406, f"Order number {order_no} is already in use for Trail ID {trail_id}")

    existing_entry = Trail_location_Point.query.filter_by(Trail_ID=trail_id, Location_point=new_locationPoint.Location_Point).one_or_none()
    if existing_entry:
        abort(406, f"Location point with trail ID {trail_id} and order number {order_no} already exists.")

    trail_location = Trail_location_Point(Trail_ID=trail_id, Location_point=new_locationPoint.Location_Point, Order_no=order_no)

    db.session.add(trail_location)
    db.session.commit()

    schema = LocationPointSchema()
    result = schema.dump(new_locationPoint)
    return result, 201



def update(locationPoint_id, locationPoint):

    if locationPoint is None:
        abort(400, "Request body is missing location point data")
    if "latitude" not in locationPoint or "longitude" not in locationPoint:
        abort(400, "Missing required fields: latitude, longitude")

    existing_locationPoint = LocationPoint.query.filter(LocationPoint.id == locationPoint_id).one_or_none()
    if existing_locationPoint:
        locationPoint_tabele_only = {
            "latitude": locationPoint["latitude"],
            "longitude": locationPoint["longitude"],
            "description": locationPoint.get("description")
        }
        locationPoint_schema_self = LocationPointSchema()
        update_locationPoint = locationPoint_schema_self.load(data=locationPoint_tabele_only, session=db.session)
        existing_locationPoint.latitude = update_locationPoint.latitude
        existing_locationPoint.longitude = update_locationPoint.longitude
        existing_locationPoint.description = update_locationPoint.description
        db.session.merge(existing_locationPoint)
        db.session.commit()
        return locationPoint_schema_self.dump(existing_locationPoint), 201
    else:
        abort(404, f"Location point with id {locationPoint_id} not found")



def delete(locationPoint_id):
    existing_locationPoint = LocationPoint.query.filter(LocationPoint.id == locationPoint_id).one_or_none()
    if existing_locationPoint:
        db.session.delete(existing_locationPoint)