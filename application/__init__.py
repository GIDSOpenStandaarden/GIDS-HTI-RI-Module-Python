"""
The main Flask application package. This application makes use of blueprints.
"""
from application.app import create_app

# Global reference to the application, use 'from flask import current_app' to reference
# this instance in dependent code, like the views and services.
app = create_app()
