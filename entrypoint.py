"""
Server module for running this application with Docker
"""
from waitress import serve

from application import create_app
from init_database import init_database

serve(init_database(create_app()), host='0.0.0.0', port=8080)
