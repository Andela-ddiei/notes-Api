import os
from flask import Flask
from flask_restful import Api
from notes import (
  NoteResource, NotesResourceDetail, UserResource,
  AuthResource, UserResourceDetail)
from application import app

api = Api(app)

api.add_resource(NoteResource, '/notes')
api.add_resource(NotesResourceDetail, '/notes/<int:note_id>')
api.add_resource(UserResource, '/users')
api.add_resource(AuthResource, '/users/login')
api.add_resource(UserResourceDetail, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
