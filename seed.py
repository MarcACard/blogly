"""Seed file to make sample data for db."""

from flask.helpers import stream_with_context
from models import User, Post, db
from app import app
from datetime import datetime

# Drop & Create
db.drop_all()
db.create_all()

# Sample Users
sam = User(first_name="Sam", last_name="San Agustin")
alex = User(first_name="Alex", last_name="Huyn")
marc = User(first_name="Marc", last_name="Card")

# Sample Posts
p1 = Post(
    title="How Not to Land a Plane",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean mollis rutrum ipsum, sit amet semper ante egestas non. Proin lacus ante, vulputate vestibulum hendrerit quis, mollis at risus. Vestibulum cursus ante dui. Etiam vel iaculis quam. Pellentesque malesuada quam mauris, non fringilla nibh porttitor vitae. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sed libero nisl. Sed et pellentesque",
    created_at=datetime(2019, 8, 13),
    user_id="1",
)
p2 = Post(
    title="Is Ball Life?",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean mollis rutrum ipsum. \n \n Sit amet semper ante egestas non. Proin lacus ante, vulputate vestibulum hendrerit quis, mollis at risus. Vestibulum cursus ante dui. Etiam vel iaculis quam. Pellentesque malesuada quam mauris, non fringilla nibh porttitor vitae. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sed libero nisl. Sed et pellentesque",
    created_at=datetime(2020, 5, 23),
    user_id="2",
)
p3 = Post(
    title="Top 3 Podcasts of 2021",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean mollis rutrum ipsum, sit amet semper ante egestas non. Proin lacus ante, vulputate vestibulum hendrerit quis, mollis at risus. Vestibulum cursus ante dui. Etiam vel iaculis quam. Pellentesque malesuada quam mauris, non fringilla nibh porttitor vitae. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sed libero nisl. Sed et pellentesque",
    created_at=datetime(2021, 12, 3),
    user_id="3",
)
p4 = Post(
    title="Network Effects Explained",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean mollis rutrum ipsum, sit amet semper ante egestas non. Proin lacus ante, vulputate vestibulum hendrerit quis, mollis at risus. Vestibulum cursus ante dui. Etiam vel iaculis quam. Pellentesque malesuada quam mauris, non fringilla nibh porttitor vitae. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sed libero nisl. Sed et pellentesque",
    created_at=datetime(2021, 1, 6),
    user_id="3",
)

# Add to Sample Users to DB
db.session.add_all([sam, alex, marc])
db.session.commit()

# Add posts to DB
db.session.add_all([p1, p2, p3, p4])
db.session.commit()
