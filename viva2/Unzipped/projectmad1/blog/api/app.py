from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from models import *
from werkzeug.exceptions import HTTPException, NotFound
import json
import datetime
import werkzeug
import base64

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_setup(app)



api = Api(app)


# Validations
class NotFoundError(HTTPException):
    def __init__(self, status_code, message=''):
        self.response = make_response(message, status_code)


class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_message):
        message = {"error_message": error_message}
        self.response = make_response(json.dumps(message), status_code)

# Output Fields in JSON Format
user_fields = {
    "name": fields.String,
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
}

# Create Parsers to handle data in request body
update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument("username")
update_user_parser.add_argument("name")
update_user_parser.add_argument("email")
update_user_parser.add_argument("password")

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument("username")
create_user_parser.add_argument("name")
create_user_parser.add_argument("email")
create_user_parser.add_argument("password")

post_parser = reqparse.RequestParser()
post_parser.add_argument("username", type=str, location='form')
post_parser.add_argument("title", type=str, location='form')
post_parser.add_argument("body", type=str, location='form')
post_parser.add_argument("date", type=str, location='form')
post_parser.add_argument("img", type=werkzeug.datastructures.FileStorage, location='files')


update_parser = reqparse.RequestParser()
update_parser.add_argument("body")
update_parser.add_argument("title")



class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self, username):
        # Get the user details from the database
        user = User.query.filter(User.username == username).scalar()

        if user:
            return user
        else:
            # Return 404 Error
            raise NotFoundError(status_code=404)

    # @marshal_with(user_fields)
    def put(self, username):  # Update
        user = User.query.filter(User.username == username).scalar()

        if user is None:
            raise NotFoundError(status_code=404)

        # Get the data from request body
        args = update_user_parser.parse_args()
        username = args.get("username", None)
        name = args.get("name", None)
        email = args.get("email", None)
        password = args.get("password", None)

        if ((email is None) or (email.isnumeric())) and (username is None) and (password is None) and ((name is None) or (name.isnumeric())):
            raise BusinessValidationError(
                status_code=400,
                error_message="One field is required!"
            )
 
        # if (name is None) or (name.isnumeric()):
        #     raise BusinessValidationError(
        #         status_code=400,
        #         error_message="Name is required and should be string."
        #     )

        # if :
        #     raise BusinessValidationError(
        #         status_code=400,
        #         error_message="Password can't be empty."
        #     )

        if (name is not None):
            user.name = name

        if (email is not None):
            user.email = email

        if (username is not None):
            user.username = username

        if (password is not None):
            user.password = password

        if (password is not None):
            if (len(password) == 6):
                pass1 = password[0:4]
                pass2 = password[4:7]
                for i in range(0,len(pass1)):
                    isinstance(pass1[i], str)
                for j in range(0, len(pass2)):
                    pass2[j].isnumeric(())


        

        # user.username = username
        # user.name = name
        # user.password = password
        # user.email = email
        db.session.commit()
        return "user updated!", 201
        

    def delete(self, username):
        # check if user exists
        user = User.query.filter(User.username == username).scalar()

        if user is None:
            raise NotFoundError(status_code=404)

        db.session.delete(user)
        db.session.commit()
        return "", 200


    def post(self):
        # Get the data from request body
        args = create_user_parser.parse_args()
        username = args.get("username", None)
        name = args.get("name", None)
        password = args.get("password", None)
        email = args.get("email", None)
        # print(password)
        user = User.query.filter(
            User.email == email).scalar()
        
        # print(username, name, password, email)

        if user is not None:
            return "", 409

        if (username is None) or (username.isnumeric()):
            raise BusinessValidationError(
                status_code=400,
                error_message="Username is required and should be string."
            )

        if (name is None) or (name.isnumeric()):
            raise BusinessValidationError(
                status_code=400,
                error_message="Name is required and should be string."
            )

        if (password is None):
            raise BusinessValidationError(
                status_code=400,
                error_message="Field can't be empty."
            )

        if (email is None) or (email.isnumeric()):
            raise BusinessValidationError(
                status_code=400,
                error_message="email is required and should be string."
            )

        user = User(
            username=username,
            name=name,
            password=password,
            email=email
        )

        db.session.add(user)
        db.session.commit()

        user = User.query.filter(User.email == email).one()

        return "user created!", 201

class Newsfeed(Resource):
    def get(self, username):
        posts = BlogPost.query.order_by(desc(BlogPost.date))
        # print(len(posts))
        allpost = []
        user = User.query.filter_by(username=username).scalar()
        following = user.followers
        
        for post in posts:
            if len(following) > 0:
            # print(len(following))

            
                
                for ids in following:
                    # print("-")
                    # print(post.author_username, post.post_id)
                    if post.author_username == ids.followed_username or post.author_username == username :
                        allpost.append(post)
                        # print("hello")

            else:
                
                if post.author_username == username:
                    allpost.append(post)
        # print(len(allpost))

        record = []
        for i in allpost:
            if i.img:
                string = i.img
                img_data = base64.b64encode(string)
                encoded_img = img_data.decode('UTF-8')
                data = {'post_id': i.post_id, 'username': i.author_username, 'img': encoded_img, 'title': i.title, 'body': i.body, 'date': i.date}
                record.append(data)
            else:
                data = {'post_id': i.post_id, 'username': i.author_username, 'title': i.title, 'body': i.body, 'date': i.date}
                record.append(data)
        # print(len(record))
        return jsonify(record)



class PostItem(Resource):
    def get(self, post_id):
        post = BlogPost.query.filter(BlogPost.post_id == post_id).scalar()
        if post is None:
            return "Post not found", 404
        else:
            if post.img:
                str = post.img
                img = base64.b64encode(str)
                # print(img.decode('UTF-8'))
                encoded_img = img.decode('UTF-8')
                return {'post_id':post.post_id,'author_username':post.author_username,'title':post.title,'body': post.body, 'img':encoded_img}
            else:
                return {'post_id':post.post_id,'author_username':post.author_username,'title':post.title,'body': post.body}


    def put(self, post_id):
        post = BlogPost.query.get(post_id)
        if post is None:
            return "Post not found", 404

        args = update_parser.parse_args()
        title = args.get('title', None)
        body = args.get('body', None)

        # data = request.get_json()

        if title :
            post.title = title

        if body:
            post.body = body 
        # print(type(title))
        # print(type(body))
        # post.title = data['title']
        # post.body = data['body']
        post.date=datetime.datetime.now()


        db.session.commit()
        post = BlogPost.query.filter()
        return '', 201


    def delete(self, post_id):
        post = BlogPost.query.get(post_id)
        if post is None:
            return "Post not found", 404
        db.session.delete(post)
        db.session.commit()
        return '', 204

    def post(self):
        args = post_parser.parse_args()

        img = args.get('img')
        title = args.get('title')
        body = args.get('body')
        date = args.get('date')
        username = args.get('username')

        # print(username)
        # print(title)

        if not username:
            return "provide the username", 400

        if not title and body and img:
            return "provide the title and body and img", 400

        if img:
            # Get the byte content using `.read()`
            image = img.read() 
            post = BlogPost(
            author_username=username,
            title=title,
            date=date,
            body=body,
            img=image
        )

            db.session.add(post)
            db.session.commit()

            return "Yay, you sent an image!", 201
        
        post = BlogPost(
            author_username=username,
            title=title,
            date=date,
            body=body
        )
        db.session.add(post)
        db.session.commit()

        
        return "POST CREATED!!", 201


class Commentpost(Resource):
    def get(self, comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            return {'id': comment.id, 'username': comment.username, 'text': comment.text}
        return {'message': 'Comment not found'}, 404

    def post(self):
        data = request.get_json()
        comment = Comment(author=data['author'], text=data['text'])
        db.session.add(comment)
        db.session.commit()
        return {'id': comment.id, 'username': comment.username, 'text': comment.text}, 201

    def put(self, comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            data = request.get_json()
            comment.username = data.get('username', comment.username)
            comment.text = data.get('text', comment.text)
            db.session.commit()
            return {'id': comment.id, 'username': comment.username, 'text': comment.text}
        return {'message': 'Comment not found'}, 404

    def delete(self, comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return {'message': 'Comment deleted'}, 200
        return {'message': 'Comment not found'}, 404


class Likepost(Resource):
    def get(self, like_id):
        # print(like_id)
        like = Like.query.get(like_id)
        if like:
            return {'username': like.username, 'post_id': like.post_id}, 200
        return {'message': 'Like not found'}, 404

    def post(self, like_id):
        data = request.get_json()
        if 'username' not in data or 'post_id' not in data:
            return {'message': 'Bad request'}, 400
        if Like.query.get(like_id):
            return {'message': 'Like already exists'}, 400
        like = Like(id=like_id, username=data['username'], post_id=data['post_id'])
        db.session.add(like)
        db.session.commit()
        return {'username': like.username, 'post_id': like.post_id}, 201

    def delete(self, like_id):
        like = Like.query.get(like_id)
        if not like:
            return {'message': 'Like not found'}, 404
        db.session.delete(like)
        db.session.commit()
        return {'message': 'Like deleted'}, 200


class FollowAPI(Resource):
    def get(self, username):
        followed = Follow.query.filter_by(follower_username=username).all()
        follower = Follow.query.filter_by(followed_username=username).all()
        # if followed and follower:
        return jsonify([{"follower":people.follower_username} for people in follower ],[{"followed":people.followed_username} for people in followed ])
        # else:
            # return "no follo"

    def post(self):
        data = request.get_json()
        follower = User.query.filter_by(username=data['follower']).first()
        followed = User.query.filter_by(username=data['followed']).first()

        # print(follower,followed)
        if follower and followed:
            follow = Follow(follower_username=follower.username, followed_username=followed.username)
            db.session.add(follow)
            db.session.commit()
            return {'message': 'Follow successful'}, 201
        return {'message': 'Follow not successful'}, 400

    def delete(self):
        data = request.get_json()
        follower = User.query.filter_by(username=data['follower']).first()
        followed = User.query.filter_by(username=data['followed']).first()
        if follower and followed:
            follow = Follow.query.filter_by(follower_username=follower.username, followed_username=followed.username).first()
            if follow:
                db.session.delete(follow)
                db.session.commit()
                return {'message': 'Unfollow successful'}, 200
            else:
                return "", 404

        return {'message': 'Unfollow not successful'}, 400

class Search(Resource):
    def get(self):
        data = request.get_json()
        search_str = data['find']
        users = User.query.filter(User.username.like('%' + search_str + '%')).all()
        l = []
        if len(users) < 1:
            return jsonify([]), 200

     
        return jsonify([{ 'username': n.username} for n in users])

class Profile(Resource):
    def get(self, username):
        posts = BlogPost.query.order_by(desc(BlogPost.date))
        allposts = []
        for post in posts:
            if post.author_username == username:
                allposts.append(post)
            
        record = []
        for i in allposts:
            if i.img:
                string = i.img
                img_data = base64.b64encode(string)
                encoded_img = img_data.decode('UTF-8')
                data = {'post_id': i.post_id, 'username': i.author_username, 'img': encoded_img, 'title': i.title, 'body': i.body, 'date': i.date}
                record.append(data)
            else:
                data = {'post_id': i.post_id, 'username': i.author_username, 'title': i.title, 'body': i.body, 'date': i.date}
                record.append(data)

        return jsonify(record)

class Userpost(Resource):
    def get(self, username):
        posts = BlogPost.query.order_by(desc(BlogPost.date))
        allposts = []
        for post in posts:
            if post.author_username == username:
                allposts.append(post)

        record = []
        for i in allposts:
            if i.img:
                string = i.img
                img_data = base64.b64encode(string)
                encoded_img = img_data.decode('UTF-8')
                data = {'post_id': i.post_id, 'username': i.author_username, 'img': encoded_img, 'title': i.title, 'body': i.body, 'date': i.date}
                record.append(data)
            else:
                data = {'post_id': i.post_id, 'username': i.author_username, 'title': i.title, 'body': i.body, 'date': i.date}
                record.append(data)

        return jsonify(record)

class Allusers(Resource):
    def get(self):
        all = User.query.all()
        return jsonify([{ 'name': n.name, 'username': n.username, 'email': n.email} for n in all])


api.add_resource(PostItem,'/posts', '/posts/<int:post_id>')

api.add_resource(UserAPI, "/user", "/user/<string:username>")

api.add_resource(Userpost, "/userpost/<string:username>")

api.add_resource(Commentpost, "/comments", "/comments/<string:comment_id>")

api.add_resource(Likepost, '/likes/<int:like_id>')

api.add_resource(FollowAPI, '/follow', '/follow/<string:username>')

api.add_resource(Search, '/search')

api.add_resource(Newsfeed, '/feed/<string:username>')

api.add_resource(Profile, '/profile/<string:username>')

api.add_resource(Allusers, '/allusers')


if __name__ == "__main__":
  app.run(
      debug=True,
      port=5000
  )