"""Seed file to make sample data for db."""

from flask.helpers import stream_with_context
from models import User, db
from app import app

# Drop & Create
db.drop_all()
db.create_all()

# == Sample Users
sam = User(first_name="Sam", last_name="San Agustin")
alex = User(first_name="Alex", last_name="Huyn")
marc = User(first_name="Marc", last_name="Card")


# == Add to Sample Users to DB
db.session.add_all([sam, alex, marc])
db.session.commit()
