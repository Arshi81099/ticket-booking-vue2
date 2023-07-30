import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def db_setup(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()
        create_admin()

def create_admin():
    user = User.query.filter(User.email == "admin@admin.com").scalar()
    if not user:
        admin = User(email="admin@admin.com", name="admin", password="admin")
        db.session.add(admin)
        db.session.commit()

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    book_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    show_date = db.Column(db.Date, nullable=False)
    show_time = db.Column(db.String, nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False)

    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    bookings = db.relationship('Book', cascade='all, delete', backref='user_', lazy=True)

class Show(db.Model):
    __tablename__ = "show"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    tag = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    img = db.Column(db.Text)
    rating = db.Column(db.Float)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)

    theatre_code = db.Column(db.Integer, db.ForeignKey('theatre.code'), nullable=False)
    bookings = db.relationship('Book', cascade='all, delete', backref='show_', lazy=True)

class Theatre(db.Model):
    __tablename__ = "theatre"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    capacity = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    code = db.Column(db.String, unique=True, nullable=False)

    bookings = db.relationship('Book', cascade='all, delete', backref='theatre_', lazy=True)
    shows = db.relationship('Show', cascade='all, delete', backref='theatre', lazy=True)
