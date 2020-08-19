"""
The database definition, the db object is a Singleton database reference, in the app.ethod create_app
this reference gets initialized with the application.
"""
from flask_sqlalchemy import SQLAlchemy
#
db: SQLAlchemy = SQLAlchemy()
