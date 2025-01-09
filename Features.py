
from multiprocessing.reduction import duplicate
import requests
import json

from flask import abort, make_response, Blueprint
from pyexpat import features

from token_checker import check_for_token, role_req
from config import db
from models import Feature, Feature_schema, Trail_feature, Trail_feature_schema
from sqlalchemy.orm import joinedload

features_bp = Blueprint("features", __name__)

@features_bp.route("/features", methods=["GET"])
@check_for_token
@role_req("User", "Administrator")
def read_all():
    features = Feature.query.all()
    schema = Feature_schema(many=True)
    result = schema.dump(features)
    if result is None:
        abort(404, "No features found")
    return result

@features_bp.route("/features/<feature_id>", methods=["GET"])
@check_for_token
@role_req("User", "Administrator")
def read_one(feature_id):
    feature = Feature.query.get(feature_id)
    schema = Feature_schema()
    result = schema.dump(feature)
    if result is None:
        abort(404, f"Feature with id {feature_id} not found")
    return result

@features_bp.route("/features", methods=["POST"])
@check_for_token
@role_req("Administrator")
def create(feature):
    print(feature)
    if feature is None:
        abort(400, "Request body is missing feature data")

    feature_table_only = {
        "trail_feature": feature.get("trail_feature")
    }


    feature_schema_self = Feature_schema()
    new_feature = feature_schema_self.load(data=feature_table_only, session=db.session)
    db.session.add(new_feature)
    db.session.commit()

    Trail_ID = feature.get("Trail_ID")
    if not Trail_ID:
        abort(400, "Missing required field: Trail_ID")

    trail_feature = feature.get("trail_feature")



    duplicate_feature_name = Trail_feature.query.filter_by(Trail_ID=Trail_ID, Trail_Feature_ID=new_feature.trail_feature_id).one_or_none()
    if duplicate_feature_name:
        abort(406, f"feature with name {trail_feature} already exists for Trail ID {Trail_ID}")

    Trail_features = Trail_feature(Trail_ID=Trail_ID, Trail_Feature_ID=new_feature.trail_feature_id)

    db.session.add(Trail_features)
    db.session.commit()


    result = feature_schema_self.dump(new_feature)
    return result, 201

@features_bp.route("/features/<feature_id>", methods=["PUT"])
@check_for_token
@role_req("Administrator")
def update(feature_id, feature):
    if feature is None:
        abort(400, "Request body is missing feature data")

    existing_feature = Feature.query.filter(Feature.trail_feature_id == feature_id).one_or_none()
    if existing_feature:
        feature_table_only = {
            "trail_feature": feature.get("trail_feature")
        }
        feature_schema_self = Feature_schema()
        update_feature = feature_schema_self.load(data=feature_table_only, session=db.session)
        existing_feature.trail_feature = update_feature.trail_feature

        # existing_trail_feature = Trail_feature.query.filter(Trail_feature.Trail_ID == feature.get("Trail_ID")).one_or_none()
        # etf_schema = Trail_feature_schema()
        # etf_result = etf_schema.dump(existing_trail_feature)
        # existing_trail_feature.Trail_Feature_ID = etf_result.trail_feature_id
        db.session.merge(existing_feature)
        db.session.commit()
        return feature_schema_self.dump(existing_feature), 201
    else:
        abort(404, f"Feature with id {feature_id} not found")
        return result, 201

@features_bp.route("/features/<feature_id>", methods=["DELETE"])
@check_for_token
@role_req("Administrator")
def delete(feature_id):
    existing_feature = Feature.query.filter(Feature.trail_feature_id == feature_id).one_or_none()
    if existing_feature:
        db.session.delete(existing_feature)
        db.session.commit()
        return make_response(f"{feature_id} successfully deleted", 200)

if __name__ == "__main__":
    token = "your_token_here"
    base_url = "http://127.0.0.1:5000/features"

    # Example 1: Get all features (Authorization header)
    response = requests.get(base_url, headers={"Authorization": f"Bearer {token}"})
    print("GET /features:", response.status_code, response.json())

    # Example 2: Get one feature by ID (Query parameter auth)
    feature_id = 1
    response = requests.get(f"{base_url}/{feature_id}?token={token}")
    print(f"GET /features/{feature_id}:", response.status_code, response.json())

    # Example 3: Create a feature (Authorization header)
    new_feature = {
        "trail_feature": "New Feature Name",
        "Trail_ID": 123
    }
    response = requests.post(base_url, json=new_feature, headers={"Authorization": f"Bearer {token}"})
    print("POST /features:", response.status_code, response.json())

    # Example 4: Update a feature by ID (Authorization header)
    feature_to_update = {
        "trail_feature": "Updated Feature Name"
    }
    response = requests.put(f"{base_url}/{feature_id}", json=feature_to_update, headers={"Authorization": f"Bearer {token}"})
    print(f"PUT /features/{feature_id}:", response.status_code, response.json())

    # Example 5: Delete a feature by ID (Query parameter auth)
    response = requests.delete(f"{base_url}/{feature_id}?token={token}")
    print(f"DELETE /features/{feature_id}:", response.status_code, response.text)
