from flask import Blueprint
from Features import features_bp  # Import only the blueprint


def register_blueprints(app):
    """Function to register all app blueprints."""
    app.register_blueprint(features_bp, url_prefix="/api/features")
