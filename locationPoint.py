from flask import abort, make_response, Blueprint

from config import db
from models import LocationPoint, LocationPointSchema, Trail, Trail_location_Point, Trailschema
from sqlalchemy.orm import joinedload

from token_checker import role_req


#these are functions that could be implemented, but most arent used
@role_req(
    "User",
    "Administrator"
)
def read_all(): #no need to read all of the location points
    '''locationPoints = LocationPoint.query.all()
    schema = LocationPointSchema(many=True)
    result = schema.dump(locationPoints)'''
    trails = Trail.query.options(
        joinedload(Trail.Trail_location_point).joinedload(Trail_location_Point.location_point_obj)
    ).all()

    schema = Trailschema(many=True)
    result = schema.dump(trails)

    if result is None:
        abort(404, "No location points found")
    return result

#reads one loc pt by ID
@role_req("User", "Administrator") #calls rolereq
def read_one(locationPoint_id):
    locationPoint = LocationPoint.query.get(locationPoint_id)
    schema = LocationPointSchema()
    result = schema.dump(locationPoint)
    if result is None:
        abort(404, f"Location point with id {locationPoint_id} not found") #Error check
    return result

#calls role_req
# creates a new trail point
@role_req("Administrator")
def create(locationPoint):
    print(locationPoint)

    #checks the right info is there, as this fucntion also adds data to other tables
    if locationPoint is None:
        abort(400, "Request body is missing location point data")
    if "latitude" not in locationPoint or "longitude" not in locationPoint:
        abort(400, "Missing required fields: latitude, longitude")

    #data for just locPt table
    locationPoint_tabele_only = {
        "latitude": locationPoint["latitude"],
        "longitude": locationPoint["longitude"],
        "description": locationPoint.get("description")
    }

    #add above data
    locationPoint_schema_self = LocationPointSchema()
    new_locationPoint = locationPoint_schema_self.load(data=locationPoint_tabele_only, session=db.session)
    db.session.add(new_locationPoint)
    db.session.commit()

    #gets the trail thats referenced
    trail_id = locationPoint.get("Trail_ID")
    if not trail_id:
        trail = Trail.query.get(trail_id)
        if not trail:
            abort(404, f"Trail with id {trail_id} not found") #reports if no trail exists

        abort(400, "Missing required field: Trail_ID")

    order_no = locationPoint.get("Order_no", 0)

    #no dupe ordernumn
    duplicate_order_no = Trail_location_Point.query.filter_by(Trail_ID=trail_id, Order_no=order_no).one_or_none()
    if duplicate_order_no:
        abort(406, f"Order number {order_no} is already in use for Trail ID {trail_id}")

    #checks for dupes
    existing_entry = Trail_location_Point.query.filter_by(Trail_ID=trail_id, Location_Point=new_locationPoint.Location_Point).one_or_none()
    if existing_entry:
        abort(406, f"Location point with trail ID {trail_id} and order number {order_no} already exists.")

    trail_location = Trail_location_Point(Trail_ID=trail_id, Location_Point=new_locationPoint.Location_Point, Order_no=order_no)

    db.session.add(trail_location)
    db.session.commit()

    schema = LocationPointSchema()
    result = schema.dump(new_locationPoint)
    return result, 201


#Update function
@role_req("Administrator")
def update(locationPoint_id, locationPoint):

    #existance checks
    if locationPoint is None:
        abort(400, "Request body is missing location point data")
    if "latitude" not in locationPoint or "longitude" not in locationPoint:
        abort(400, "Missing required fields: latitude, longitude")

    #checks original table and then writes the JSON data to all involved tabels
    existing_locationPoint = LocationPoint.query.filter(LocationPoint.Location_Point == locationPoint_id).one_or_none()
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



#Admin only delete
@role_req("Administrator")
def delete(locationPoint_id):
    existing_locationPoint = LocationPoint.query.filter(LocationPoint.Location_Point == locationPoint_id).one_or_none()

    if not existing_locationPoint:
        abort(404, f"Location point with id {locationPoint_id} not found")

    # Trail_loc_point = Trail_location_Point.query.filter(Trail_location_Point.Location_Point == locationPoint_id).one_or_none()
    # if Trail_loc_point:
    #     db.session.delete(Trail_loc_point)
    #     db.session.commit()
    if not existing_locationPoint:
        abort(404, f"Location point with id {locationPoint_id} not found")

    if existing_locationPoint:
        db.session.delete(existing_locationPoint)
        db.session.commit()
        return make_response(f"{locationPoint_id} successfully deleted", 200)