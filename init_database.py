"""
Script to initialize a clean database.
"""

from application.database import db


def init_database(app):
    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    from application import app

    init_database(app)
