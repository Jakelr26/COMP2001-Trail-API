import os
from multiprocessing.reduction import duplicate
import requests
import json
import sys
from flask import abort, make_response, Blueprint
from pyexpat import features
from cryptography.fernet import Fernet
import json

from token_checker import role_req
from config import db
from models import Feature, Feature_schema, Trail_feature, Trail_feature_schema
from sqlalchemy.orm import joinedload




# @check_for_token
@role_req("User", "Administrator")
def read_all():

    features = Feature.query.all()
    schema = Feature_schema(many=True)
    result = schema.dump(features)
    if result is None:
        abort(404, "No features found")
    return result

# @check_for_token
@role_req("User", "Administrator")
def read_one(feature_id):
    feature = Feature.query.get(feature_id)
    schema = Feature_schema()
    result = schema.dump(feature)
    if result is None:
        abort(404, f"Feature with id {feature_id} not found")
    return result

# @check_for_token
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

# @check_for_token
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

# @check_for_token
@role_req("Administrator")
def delete(feature_id):
    existing_feature = Feature.query.filter(Feature.trail_feature_id == feature_id).one_or_none()
    if existing_feature:
        db.session.delete(existing_feature)
        db.session.commit()
        return make_response(f"{feature_id} successfully deleted", 200)


