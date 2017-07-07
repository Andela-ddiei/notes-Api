from flask_sqlalchemy import SQLAlchemy
from notes import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Note(db.Model):
    __tablename__ = "Notes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    content = db.Column(db.String(140), unique=True)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Note %r>' % self.title
