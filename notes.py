from flask import request, jsonify
from flask_restful import fields, marshal, Resource, reqparse
from flask_httpauth import HTTPBasicAuth
from models import Note, User, db

auth = HTTPBasicAuth()


@auth.verify_password
def verify_token(username, password):
    data = User.verify_token(request.headers.get('Authorization') or "")
    if data:
        user = User.query.get(data['id'])
        return user
    else:
        return False


class NoteResource(Resource):
    new_dict = {
        "id": fields.Integer,
        "title": fields.String,
        "content": fields.String,
        "user_id": fields.Integer
    }

    @auth.login_required
    def get(self):
        notes = Note.query.all()
        if notes:
            return marshal(notes, self.new_dict), 200
        else:
            return {"message": "No notes have been created"}, 200

    @auth.login_required
    def post(self):
        if not request.json:
            return {"message": "Request must be valid JSON"}, 400

        user = User.verify_token(request.headers.get('Authorization'))

        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('content')

        args = parser.parse_args()

        if not args["title"] or not args["content"]:
            return {"message": "Request must contain title and content"}, 400

        new_note = Note(args["title"], args["content"])
        new_note.user_id = user["id"]

        db.session.add(new_note)
        db.session.commit()

        return marshal(new_note, self.new_dict), 201


class NotesResourceDetail(Resource):
    new_dict = {
        "id": fields.Integer,
        "title": fields.String,
        "content": fields.String
    }

    @auth.login_required
    def get(self, note_id):
        user = User.verify_token(request.headers.get('Authorization'))
        note = Note.query.get(note_id)
        if note.user_id == user["id"]:
            return marshal(note, self.new_dict), 200
        else:
            return {
                "message": "You are not authorized for this operation"
                }, 401

    @auth.login_required
    def delete(self, note_id):
        user = User.verify_token(request.headers.get('Authorization'))
        note = Note.query.get(note_id)
        if note:
            if note.user_id == user["id"]:
                db.session.delete(note)
                db.session.commit()
                return {}, 204
            else:
                return {
                    "message":
                        ("You are not authorized to carry out this operation")},
                401
        else:
            return{"message": "Note does not exist"}, 404

    @auth.login_required
    def put(self, note_id):
        if not request.json:
            return {"message": "Request must be valid JSON"}, 400

        note = Note.query.get(note_id)
        if note:
            parser = reqparse.RequestParser()
            parser.add_argument('title')
            parser.add_argument('content')

            args = parser.parse_args()
            if args["title"]:
                note.title = args["title"]
            if args["content"]:
                note.content = args["content"]

            db.session.add(note)
            db.session.commit()

            return marshal(note, self.new_dict), 200
        else:
            return{"message": "Note does not exist"}, 404


class UserResource(Resource):
    new_dict = {
        "id": fields.Integer,
        "username": fields.String
    }

    @auth.login_required
    def get(self):
        users = User.query.all()
        if users:
            return marshal(users, self.new_dict), 200
        else:
            return {"message": "No users exist"}, 200

    def post(self):
        if not request.json:
            return {"message": "Request must be valid JSON"}, 400

        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')

        args = parser.parse_args()
        if not args["username"] or not args["password"]:
            return {
                "message": "Request must contain a username and a password"
                }, 400

        hashed_password = User.hash_password(args["password"])
        new_user = User(args["username"], hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return marshal(new_user, self.new_dict), 201


class UserResourceDetail(Resource):
    new_dict = {
        "id": fields.Integer,
        "username": fields.String
    }

    @auth.login_required
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return marshal(user, self.new_dict), 200
        else:
            return {"message": "This user does not exist"}, 404

    @auth.login_required
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

            return {}, 204
        else:
            return {"message": "This user does not exist"}, 404


class AuthResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')

        args = parser.parse_args()
        user = User.query.filter_by(username=args["username"]).first()

        if user:
            if user.verify_hash(args["password"], user.password):
                token = user.generate_auth_token().decode("ascii")
                return {"token": token}, 200
            else:
                return {"message": "Invalid password"}, 403
        else:
            return {"message": "This user does not exist"}, 404
