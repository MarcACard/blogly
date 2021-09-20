"""Seed file to make sample data for db."""

from models import User, Post, db, Tag
from app import app

# Drop & Create
db.drop_all()
db.create_all()

# Sample Users
sam = User(first_name="Sam", last_name="San Agustin")
alex = User(first_name="Alex", last_name="Huynh")
marc = User(first_name="Marc", last_name="Card")

# Sample Posts
p1 = Post(
    title="How Not to Land a Plane",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean mollis rutrum ipsum, sit amet semper ante egestas non. Proin lacus ante, vulputate vestibulum hendrerit quis, mollis at risus. Vestibulum cursus ante dui. Etiam vel iaculis quam. Pellentesque malesuada quam mauris, non fringilla nibh porttitor vitae. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sed libero nisl. Sed et pellentesque",
    user_id="1",
)
p2 = Post(
    title="Is Ball Life?",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean mollis rutrum ipsum. Sit amet semper ante egestas non. Proin lacus ante, vulputate vestibulum hendrerit quis, mollis at risus. Vestibulum cursus ante dui. Etiam vel iaculis quam. Pellentesque malesuada quam mauris, non fringilla nibh porttitor vitae. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sed libero nisl. Sed et pellentesque",
    user_id="2",
)
p3 = Post(
    title="Top 3 Podcasts of 2021",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean mollis rutrum ipsum, sit amet semper ante egestas non. Proin lacus ante, vulputate vestibulum hendrerit quis, mollis at risus. Vestibulum cursus ante dui. Etiam vel iaculis quam. Pellentesque malesuada quam mauris, non fringilla nibh porttitor vitae. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sed libero nisl. Sed et pellentesque",
    user_id="3",
)
p4 = Post(
    title="Network Effects Explained",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean mollis rutrum ipsum, sit amet semper ante egestas non. Proin lacus ante, vulputate vestibulum hendrerit quis, mollis at risus. Vestibulum cursus ante dui. Etiam vel iaculis quam. Pellentesque malesuada quam mauris, non fringilla nibh porttitor vitae. Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sed libero nisl. Sed et pellentesque",
    user_id="3",
)

# Add some Tags
t1 = Tag(name="basketball")
t2 = Tag(name="planes")

p1.tags.append(t2)
p2.tags.append(t1)

# Add to Sample Users to DB
db.session.add_all([sam, alex, marc])
db.session.commit()

# Add posts to DB
db.session.add_all([p1, p2, p3, p4])
db.session.commit()
