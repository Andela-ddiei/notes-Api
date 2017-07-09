from flask import Flask
from flask_restful import fields, marshal_with, Resource, Api, reqparse

app = Flask(__name__)

api = Api(app)

from models import Note, db


@app.route("/")
def hello():
    return "Hello World!"


class NoteResource(Resource):
    new_dict = {
        "id": fields.Integer,
        "title": fields.String,
        "content": fields.String
    }

    @marshal_with(new_dict)
    def get(self):
        notes = Note.query.all()
        return notes, 200

    @marshal_with(new_dict)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('content')

        args = parser.parse_args()

        new_note = Note(args["title"], args["content"])
        db.session.add(new_note)
        db.session.commit()

        return new_note, 201


class NotesResourceDetail(Resource):
    new_dict = {
        "id": fields.Integer,
        "title": fields.String,
        "content": fields.String
    }

    @marshal_with(new_dict)
    def get(self, note_id):
        note = Note.query.get(note_id)
        return note, 200

    def delete(self, note_id):
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()

        return {}, 204

    @marshal_with(new_dict)
    def put(self, note_id):
        note = Note.query.get(note_id)

        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('content')

        args = parser.parse_args()

        note.title = args["title"]
        note.content = args["content"]

        db.session.add(note)
        db.session.commit()

        return note, 200

api.add_resource(NoteResource, '/notes')
api.add_resource(NotesResourceDetail, '/notes/<int:note_id>')