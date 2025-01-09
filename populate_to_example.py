from config import db
from models import (
    Feature, Trail_feature, LocationPoint, Trail_location_Point, User_tabel, Trail
)


# Example to populate data in the Feature table
def populate_features():
    features_data = [
        {"trail_feature_id": 1, "trail_feature": "Waterfall"},
        {"trail_feature_id": 2, "trail_feature": "Mountain View"},
    ]
    for feature in features_data:
        new_feature = Feature(
            trail_feature_id=feature["trail_feature_id"],
            trail_feature=feature["trail_feature"]
        )
        db.session.add(new_feature)
    db.session.commit()
    print("Feature table populated.")


# Example to populate data in the LocationPoint table
def populate_location_points():
    location_points_data = [
        {"Location_Point": 1, "latitude": 50.3763, "longitude": -4.1427, "description": "Starting Point"},
        {"Location_Point": 2, "latitude": 50.3784, "longitude": -4.1451, "description": "Scenic View"},
    ]
    for lp in location_points_data:
        new_location_point = LocationPoint(
            Location_Point=lp["Location_Point"],
            latitude=lp["latitude"],
            longitude=lp["longitude"],
            description=lp["description"]
        )
        db.session.add(new_location_point)
    db.session.commit()
    print("LocationPoint table populated.")


# Example to populate data in the User_tabel
def populate_users():
    users_data = [
        {"User_id": 1, "Email": "admin@example.com", "Role": "Administrator"},
        {"User_id": 2, "Email": "user@example.com", "Role": "User"},
    ]
    for user in users_data:
        new_user = User_tabel(
            User_id=user["User_id"],
            Email=user["Email"],
            Role=user["Role"]
        )
        db.session.add(new_user)
    db.session.commit()
    print("User_tabel table populated.")


# Example to populate data in the Trail table
def populate_trails():
    trails_data = [
        {
            "Trail_ID": 1,
            "Trail_name": "Mountain Trail",
            "Trail_summary": "A scenic mountain trail.",
            "Trail_Description": "This trail offers stunning views of the mountains and valleys.",
            "Difficulty": "Moderate",
            "Location": "Mountain Region",
            "Distance": 10,
            "Elevation": 1200,
            "Route_Type": "Loop",
            "Owner_ID": 1,
        },
        {
            "Trail_ID": 2,
            "Trail_name": "Forest Trail",
            "Trail_summary": "A calm forest trail.",
            "Trail_Description": "This trail goes through lush green forests.",
            "Difficulty": "Easy",
            "Location": "Woodland Zone",
            "Distance": 5,
            "Elevation": 200,
            "Route_Type": "Point-to-Point",
            "Owner_ID": 2,
        },
    ]
    for trail in trails_data:
        new_trail = Trail(
            Trail_ID=trail["Trail_ID"],
            Trail_name=trail["Trail_name"],
            Trail_summary=trail["Trail_summary"],
            Trail_Description=trail["Trail_Description"],
            Difficulty=trail["Difficulty"],
            Location=trail["Location"],
            Distance=trail["Distance"],
            Elevation=trail["Elevation"],
            Route_Type=trail["Route_Type"],
            Owner_ID=trail["Owner_ID"],
        )
        db.session.add(new_trail)
    db.session.commit()
    print("Trail table populated.")


# Main function to call all population methods
def populate_tables():
    print("Starting table population...")
    populate_features()
    populate_location_points()
    populate_users()
    populate_trails()
    print("All tables populated successfully!")


if __name__ == "__main__":
    # Ensure the database tables exist
    db.create_all()
    populate_tables()
