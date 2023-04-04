import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
# from app import app


db = SQLAlchemy()
def db_setup(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()


class User(db.Model):
    __tablename__="user_table"
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(250), nullable=False)
    username=db.Column(db.String(250),unique=True, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password=db.Column(db.String(250), nullable=False)

    Blogpost = db.relationship("BlogPost",cascade='all, delete', backref="User")
    comments = db.relationship("Comment",cascade='all, delete', backref="User")
    like = db.relationship("Like", cascade='all, delete', backref="User")
    followers = db.relationship('Follow',cascade='all, delete', backref='follower', lazy=True, foreign_keys='Follow.follower_username')
    following = db.relationship('Follow',cascade='all, delete', backref='followed', lazy=True, foreign_keys='Follow.followed_username')



class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    post_id = db.Column(db.Integer, primary_key=True)
    author_username = db.Column(db.String, db.ForeignKey(User.username))
    title = db.Column(db.String(250))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    body = db.Column(db.Text)
    img = db.Column(db.String(250))

    comments = db.relationship("Comment",cascade='all, delete', backref="BlogPost")
    like_author = db.relationship("Like",cascade='all, delete', backref="BlogPost")  



class Comment(db.Model):
    __tablename__ = "comments"
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    author_username = db.Column(db.String, db.ForeignKey(User.username))
    cpost_id = db.Column(db.Integer, db.ForeignKey(BlogPost.post_id))
    



class Like(db.Model):
    __tablename__ = "likes"
    like_id = db.Column(db.Integer, primary_key=True) 

    like_username = db.Column(db.String, db.ForeignKey(User.username))
    post_id = db.Column(db.Integer, db.ForeignKey(BlogPost.post_id))


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_username = db.Column(db.String, db.ForeignKey(User.username))
    followed_username = db.Column(db.String, db.ForeignKey(User.username))


