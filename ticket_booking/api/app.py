from http.client import HTTPException
import marshal
from flask import Flask, jsonify, make_response, request, render_template
from flask_mail import Mail, Message
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from sqlalchemy import desc, or_
import werkzeug
import base64
import requests
from flask_cors import CORS
from datetime import datetime, timedelta, time
import json
from models import *
import pdfkit
from celery import Celery
from celery.schedules import crontab
from redis import Redis


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Change this to a secure key in production
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

# Initialize the database
# db = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

db_setup(app)

api = Api(app)

# Initialize the Flask-Mail extension
mail = Mail(app)

# Initialize the Flask-JWT-Extended extension
jwt = JWTManager(app)

# Set a secret key for the app (change this to a secure value in production)
app.secret_key = 'your-secret-key'

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Create a Celery instance for task scheduling
celery = Celery('api', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery.conf.update(app.config)

# Redis instance for caching
redis = Redis(host='redis', port=6379)

# Validations
class NotFoundError(HTTPException):
    def __init__(self, status_code, message=''):
        self.response = make_response(message, status_code)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_message):
        message = {"error_message": error_message}
        self.response = make_response(json.dumps(message), status_code)

# Custom field to handle base64 encoding of the image
class Base64ImageField(fields.Raw):
    def format(self, value):
        if value:
            return base64.b64encode(value).decode('utf-8')
        return None  

# Output Fields in JSON Format

theatre_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "capacity": fields.Integer,
    "address": fields.String,
    "code": fields.String,
}

show_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "img": Base64ImageField(attribute='img'),
    "genre": fields.String,
    "tags": fields.List(fields.String),
    "time": fields.String,
    "rating": fields.Float,
    "start_date": fields.DateTime(dt_format='iso8601'),
    "end_date": fields.DateTime(dt_format='iso8601'),
    "ticket_price": fields.Float,
    "theatre_code": fields.String,
}

trending_show_fields = {
    'title': fields.String(attribute='name'),
    'show_date': fields.DateTime(dt_format='iso8601', attribute='show_date'),
    'theatre_name': fields.String(attribute='theatre_name'),
    'show_time': fields.DateTime(dt_format='iso8601', attribute='show_time')
}

user_fields = {
    "name": fields.String,
    "email": fields.String,
    "password": fields.String
}

# Decorator function to handle revoked tokens
def handle_revoked_token():
    def decorator(f):
        def wrapper(jwt_header, jwt_payload):
            return f(jwt_header, jwt_payload) if jwt_payload["jti"] in blocklist else (None, 200)

        return wrapper
    return decorator

# FOR BLACKLISTING JWT TOKENS
blocklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in blocklist


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == "admin@admin.com":
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

# Helper function to validate email and password
def validate_user(email, password):
    user = User.query.filter(User.email == email).first()
    if user and user.password == password:
        return user
    return None

# Create Parsers to handle data in request body
update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument("name")
update_user_parser.add_argument("email")
update_user_parser.add_argument("password")

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument("name")
create_user_parser.add_argument("email")
create_user_parser.add_argument("password")

theatre_parser = reqparse.RequestParser()
theatre_parser.add_argument("name")
theatre_parser.add_argument("capacity")
theatre_parser.add_argument("address")
theatre_parser.add_argument("code")

show_parser = reqparse.RequestParser()
show_parser.add_argument("name", type=str, location='form')
show_parser.add_argument("img", type=werkzeug.datastructures.FileStorage, location='files')
show_parser.add_argument("genre", type=str, location='form')
show_parser.add_argument("tags", type=str, location='form')
show_parser.add_argument("time", type=str, location='form')
show_parser.add_argument("start_date", type=str, location='form')
show_parser.add_argument("end_date", type=str, location='form')
show_parser.add_argument("ticket_price", type=str, location='form')
show_parser.add_argument("theatre_code", type=str, location='form')

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'error': 'Missing email or password'}, 400

        user = validate_user(email, password)
        if not user:
            return {'error': 'Invalid username or password'}, 401

        access_token = create_access_token(identity=user.email)
        return {'access_token': access_token}, 200

class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        blocklist.add(jti)
        return {"message": "Successfully logged out"}, 200

class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self):
        # args = create_user_parser.parse_args()
        email = request.args.get('email', None)
        user = User.query.filter(User.email == email).scalar()

        if user:
            return user
        else:
            raise NotFoundError(status_code=404)

    def put(self): 
        args = create_user_parser.parse_args()

        name = args.get("name", None)
        password = args.get("password", None)
        email = args.get("email", None)
        n_email = args.get("n_email", None)

        user = User.query.filter(User.email == email).scalar()
        n_user = User.query.filter(User.email == n_email).scalar()


        if user is None:
            raise NotFoundError(status_code=404)

        if ((email is None) or (email.isnumeric())) and (password is None) and ((name is None) or (name.isnumeric())):
            raise BusinessValidationError(
                status_code=400,
                error_message="One field is required!"
            )
 
        if (name is not None):
            user.name = name

        if (n_user is not None):
            raise BusinessValidationError(
                status_code=400,
                error_message="This email is already taken!"
            )

        if (n_email is not None):
            user.email = n_email

        if (password is not None):
            user.password = password

 
        db.session.commit()
        return "User updated!", 201
        
    def delete(self):

        args = create_user_parser.parse_args()
        email = args.get('email', None)
        password = args.get('password', None)
        user = User.query.filter(User.email == email).scalar()

        if user is None:
            raise NotFoundError(status_code=404)

        db.session.delete(user)
        db.session.commit()
        return "", 200

    def post(self):
        args = create_user_parser.parse_args()

        name = args.get("name", None)
        password = args.get("password", None)
        email = args.get("email", None)

        user = User.query.filter(
            User.email == email).scalar()

        if user is not None:
            return "", 409

        if (name is None) or (name.isnumeric()):
            raise BusinessValidationError(
                status_code=400,
                error_message="Name is required and should be string."
            )

        if (password is None):
            raise BusinessValidationError(
                status_code=400,
                error_message="Password can't be empty."
            )

        if (email is None) or (email.isnumeric()):
            raise BusinessValidationError(
                status_code=400,
                error_message="Email is required and should be string."
            )

        user = User(
            name=name,
            password=password,
            email=email
        )

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.email)
        return {"message": "user created successfully", "name": name, "email": email, 'access_token': access_token}, 201

class TheatreAPI(Resource):
    def get(self, id):
        theatre = Theatre.query.filter(Theatre.id == id).scalar()

        if theatre:
            return {
                "id": theatre.id,
                "name": theatre.name,
                "capacity": theatre.capacity,
                "address": theatre.address,
                "code": theatre.code,
            }, 200
        else:
            raise NotFoundError(status_code=404)

    def put(self, code):
        theatre = Theatre.query.filter(Theatre.code == code).scalar()
        args = theatre_parser.parse_args()
        
        name = args.get('name', None)
        capacity = args.get('capacity', None)
        address = args.get('address', None)

        if (name is not None) :
            theatre.name = name
        if (capacity is not None) :
            theatre.capacity = capacity
        if (address is not None) :
            theatre.address = address


        db.session.commit()

        return 'Theatre Updated', 201

    def post(self):
        args = theatre_parser.parse_args()

        name = args.get('name', None)
        capacity = args.get('capacity', None)
        address = args.get('address', None)
        code = args.get('code', None)

        if name is None:
            return "Provide name", 400

        if (capacity is None) or not (capacity.isnumeric()):
            raise BusinessValidationError(
                status_code=400,
                error_message="Capacity is required and should be integer."
            )
        if (address is None) :
            raise BusinessValidationError(
                status_code=400,
                error_message="Address is required and should be alphanumeric."
            )

        if (code is None):
            raise BusinessValidationError(
                status_code=400,
                error_message="Code can't be empty."
            )
        theatre = Theatre(
            name=name,
            capacity=capacity,
            address=address,
            code=code
        )

        db.session.add(theatre)
        db.session.commit()

        return "Theatre created!", 201

    def delete(self, code):
        theatre = Theatre.query.filter(Theatre.code == code).scalar()

        if theatre is None:
            raise NotFoundError(status_code=404)

        db.session.delete(theatre)
        db.session.commit()
        return "", 200

class ShowAPI(Resource):
    def get(self, id):
        show = Show.query.filter(Show.id == id).scalar()
        if show:
            if show.img:
                str = show.img
                image = base64.b64encode(str)
                encoded_img = image.decode('UTF-8')
                return {
                    "id": show.id,
                    "name": show.name,
                    "img": encoded_img,
                    "genre": show.genre,
                    "tags": show.tags,
                    "time": show.time,
                    "rating": show.rating,
                    "start_date": show.start_date,
                    "end_date": show.end_date,
                    "ticket_price": show.ticket_price,
                    "theatre_code": show.theatre_code
                }, 200
            else:
                return {
                    "id": show.id,
                    "name": show.name,
                    "genre": show.genre,
                    "tags": show.tags,
                    "time": show.time,
                    "rating": show.rating,
                    "start_date": show.start_date,
                    "end_date": show.end_date,
                    "ticket_price": show.ticket_price,
                    "theatre_code": show.theatre_code
                }, 200
        else:
            raise NotFoundError(status_code=404)

    def put(self, id):
        args = show_parser.parse_args()

        name = args.get('name', None)
        img = args.get('img', None)
        genre = args.get('genre', None)
        tags = args.get('tags', None)
        time = args.get('time', None)
        start_date = args.get('start_date', None)
        end_date = args.get('end_date', None)
        ticket_price = args.get('ticket_price', None)
        theatre_code = args.get('theatre_code', None)

        show_o = Show.query.filter(Show.id == id).scalar()

        if show_o is None:
            raise NotFoundError(status_code=404)

        if name:
            show_o.name = name
        if img:
            image = image.read()
            show_o.img = image
        if genre:
            show_o.genre = genre
        if tags:
            show_o.tags = tags
        if time:
            show_o.time = time
        if start_date:
            show_o.start_date = datetime(start_date).date()
        if end_date:
            show_o.end_date = datetime(end_date).date()
        if ticket_price:
            show_o.ticket_price = ticket_price
        if theatre_code:
            show_o.theatre_code = theatre_code

        db.session.commit()
        return '', 201

    def delete(self, id):
        show = Show.query.filter(Show.id == id).scalar()
        if show is None:
            raise NotFoundError(status_code=404)

        db.session.delete(show)
        db.session.commit()
        return 'Show deleted!', 200

    def post(self):
        args = show_parser.parse_args()
        name = args.get('name', None)
        img = args.get('img',None)
        genre = args.get('genre', None)
        tags = args.get('tags', None)
        time = args.get('time', None)
        start_date = args.get('start_date', None)
        end_date = args.get('end_date', None)
        ticket_price = args.get('ticket_price', None)
        theatre_code = args.get('theatre_code', None)

        if (theatre_code is None) or (name is None) or (genre is None) or (tags is None) or (time is None) or (start_date is None) or (end_date is None) or (ticket_price is None):
            return "Field can't be empty.", 400

        theatre = theatre_code.split(',')

        if img:
            image = img.read() 
            for i in theatre:
                show = Show(name = name, img = image, genre = genre, tags = tags, time = time, start_date = start_date, end_date = end_date, ticket_price = ticket_price, theatre_code = i)
                db.session.add(show)
                db.session.commit()

        else:
            for i in theatre:
                show = Show(name = name, genre = genre, tags = tags, time = time, start_date = start_date, end_date = end_date, ticket_price = ticket_price, theatre_code = i)
                db.session.add(show)
                db.session.commit()
        
        return "SHOW CREATED!!", 201

class BookAPI(Resource):
    def post(self):
        data = request.get_json()
        book_date = data['book_date']
        show_date = data['show_date']
        show_time = data['show_time']
        seats_booked = data['seats_booked']
        theatre = data['theatre']
        show = data['show']
        user = data['show']

        theatre_capacity = Theatre.query.filter(Theatre.code == theatre).scalar()
        theatre_capacity = theatre_capacity.capacity
        total_booked = db.session.query(db.func.sum(Book.seats_booked)).filter(
            Book.theatre == theatre,
            Book.show == show,
            Book.show_date == show_date,
            Book.show_time == show_time
        ).scalar()

        avl_seats = theatre_capacity - total_booked

        if avl_seats >= seats_booked:
            book = Book(show_date=show_date, show_time=show_time, seats_booked=seats_booked, theatre=theatre, show=show, user=user)
            db.session.add(book)
            db.session.commit()
            return "Successfully booked!", 201
        else:
            raise BusinessValidationError(
                status_code=400,
                error_message=f'Only {avl_seats} seats available!'
            )

    def get(self, id):
        book = Book.query.filter(Book.id == id).scalar()
        show_id = book.show
        show = Show.query.filter(Show.id == show_id).scalar()
        if book:
            return {
                    "id": book.id,
                    "book_date": book.book_date,
                    "show_date": book.show_date,
                    "show_time": book.show_time,
                    "seats_booked": book.seats_booked,
                    "theatre": book.theatre,
                    "show_id": show_id,
                    "show_name": show.name,
                    "user": book.user
                }, 200

        else:
            raise NotFoundError(status_code=404)

class SearchAPI(Resource):
    def get(self, search_str):
        theatres = Theatre.query.filter(or_(
            Theatre.name.like('%' + search_str + '%'),
            Theatre.address.like('%' + search_str + '%')
        )).all()

        shows = Show.query.filter(or_(
            Show.name.like('%' + search_str + '%'),
            Show.genre.like('%' + search_str + '%'),
            Show.tags.like('%' + search_str + '%'),
            Show.rating.like('%' + search_str + '%')
        )).all()

        if theatres:
            theatre_data = jsonify({"theatres": marshal(theatres, theatre_fields)})
        else:
            theatre_data = jsonify({"theatres": []})

        if shows:
            show_data = jsonify({"shows": marshal(shows, show_fields)})
        else:
            show_data = jsonify({"shows": []})

        return {"theatres": theatre_data, "shows": show_data}, 200

class TheatreShowListAPI(Resource):
    @marshal_with(show_fields)
    def get(self, code):
        theatre = Theatre.query.filter(Theatre.code == code).first()
        if theatre is None:
            return {"error": "Theatre not found"}, 404

        shows = theatre.shows
        if len(shows) > 0:
            return shows, 200
        else:
            return {}, 200

class TheatreListAPI(Resource):
    @marshal_with(theatre_fields)
    def get(self):
        theatres = Theatre.query.all()
        if len(theatres) > 0:
            return theatres
        else: 
            return {}, 200

class Trending(Resource):
    @marshal_with(trending_show_fields)
    def get(self):
        trending_shows = db.session.query(
            Show.name,
            Book.show_date,
            Theatre.name.label('theatre_name'),
            Show.time.label('show_time')
        ).join(Book).join(Theatre).group_by(Show).order_by(desc(db.func.count(Book.id))).limit(10).all()

        if trending_shows is None or len(trending_shows) == 0:
            return {},200

        return trending_shows, 200
# helper functions
def is_valid_email(email):
    return email and '@' in email

def is_valid_task_id(task_id):
    return bool(task_id)

# VisitedTodayResource class
class VisitedTodayResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        now = datetime.utcnow()

        # Calculate the expiration time at the end of the current day
        expires = datetime(now.year, now.month, now.day, 23, 59, 59) + timedelta(days=1)

        # Create a response with a message and set the JWT token as a cookie
        response = make_response(jsonify({'msg': 'Visited today!'}), 200)
        response.set_cookie('jwt', create_access_token(identity=current_user), expires=expires, httponly=True)

        # Trigger the Celery task if the user has not visited until 6pm
        if now.time() <= time(hour=18) and datetime.fromtimestamp(get_jwt_identity()['iat']).date() == now.date():
            send_daily_reminder_task.apply_async()

        return response

# SendDailyReminderTask class with Celery task
@celery.task
def send_daily_reminder_task():
    now = datetime.utcnow()
    current_user = get_jwt_identity()

    # Check if the user has a valid JWT token that was issued today and has not visited your website until 6pm
    if now.time() <= time(hour=18) and datetime.fromtimestamp(current_user['iat']).date() == now.date():
        # Send a Google Chat message using a webhook
        webhook_url = 'https://chat.googleapis.com/v1/spaces/<SPACE_ID>/messages?key=<API_KEY>'
        message = {
            'text': 'Reminder: You have not visited our website today!'
        }
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()

# Report class
class Report(Resource):
    @jwt_required()
    def post(self):
        user_email = get_jwt_identity()

        # Check if the user_email is a valid email address before generating the report
        if not is_valid_email(user_email):
            return {'error': 'Invalid email address'}, 400

        # Generate the report asynchronously using Celery
        task = generate_report.apply_async(args=[user_email])

        # Return a response to the user with the task ID
        return {'task_id': task.id}, 202

# ReportStatus class
class ReportStatus(Resource):
    @jwt_required()
    def get(self, task_id):
        # Check if the task_id is valid
        if not is_valid_task_id(task_id):
            return {'error': 'Invalid task_id'}, 400

        # Check the status of the Celery task
        task = generate_report.AsyncResult(task_id)

        if task.state == 'PENDING':
            response = {
                'status': 'pending',
                'message': 'The report is not ready yet.'
            }
        elif task.state == 'SUCCESS':
            # If the task is successful, return the URL of the report
            response = {
                'status': 'success',
                'url': task.result
            }
        else:
            # If the task failed, return an error message
            response = {
                'status': 'failed',
                'message': 'There was an error generating the report.'
            }

        return jsonify(response)

@celery.task
def generate_report(user_email, form):
    user = User.query.filter_by(email=user_email).first()
    bookings = Book.query.filter_by(user_id=user.id).all()

    if form == 'html':
        html_report = generate_html_report(user, bookings)
        return html_report
    elif form == 'pdf':
        html_report = generate_html_report(user, bookings)
        pdf_report = generate_pdf_report(html_report)
        return pdf_report
    else:
        raise ValueError("Invalid report format")

def generate_html_report(user, bookings):
    report_html = render_template('user_report.html', user=user, bookings=bookings)
    return report_html

def generate_pdf_report(html_report):
    # Convert the HTML report to PDF using pdfkit
    pdf_report = pdfkit.from_string(html_report, False)
    return pdf_report

@celery.task
def send_monthly_engagement_report(email):
    user = User.query.filter_by(email=email).first()

    # Calculate the start date for the past 1 month
    start_date = datetime.now() - timedelta(days=30)

    # Query the bookings for the user within the past 1 month
    bookings = Book.query.filter(Book.user == user.id, Book.booking_date >= start_date).all()

    # Generate the HTML report template
    report_html = render_template('monthly_report.html', user=user, bookings=bookings)

    # Create the email message
    msg = Message(subject='Monthly Engagement Report',
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])

    # Set the email body as the HTML report template
    msg.html = report_html

    # Send the email
    with app.app_context():
        mail.send(msg)

    return jsonify({'message': 'Monthly engagement report sent successfully'}), 200

app.send_daily_reminder = send_daily_reminder_task

# Celery beat schedule
celery.conf.beat_schedule = {
    'send-daily-reminder': {
        'task': 'app.send_daily_reminder',
        'schedule': crontab(hour=18, minute=0, day_of_week='*')
    }
}

# Celery periodic task (monthly)
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    curr_user = get_jwt_identity()
    email = curr_user
    # Run the task every month on the 1st day at 8:00 AM UTC
    sender.add_periodic_task(crontab(day_of_month='1', hour='8', minute='0'),
                             send_monthly_engagement_report.s(email))

celery.conf.timezone = 'UTC'


api.add_resource(VisitedTodayResource, '/visited-today')
api.add_resource(Report, '/report')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(ReportStatus, '/report/<string:task_id>')
api.add_resource(TheatreListAPI, '/theatres')  # Endpoint for getting all theatres
api.add_resource(TheatreShowListAPI, '/theatres/<string:code>') 
api.add_resource(UserAPI, "/user", "/user/<string:username>")
api.add_resource(SearchAPI, '/search/<string:search_str>')
api.add_resource(Trending, '/trending')
api.add_resource(BookAPI, '/book', '/book/<int:id>')
api.add_resource(TheatreAPI, '/theatre', '/theatre/<int:code>')
api.add_resource(ShowAPI, '/show', '/show/<int:id>')
# api.add_resource(SearchAPI, '/search')


if __name__ == "__main__":
  app.run(
      debug=True,
      port=5000
  )