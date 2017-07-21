from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature
from application import app
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(140), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def hash_password(password):
        return bcrypt.hash(password)

    def verify_hash(self, password, hashed_password):
        return bcrypt.verify(password, hashed_password)

    def generate_auth_token(self):
        auth_key = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in = 60)
        token = auth_key.dumps({'id': self.id})
        return token

    @staticmethod
    def verify_token(token):
        auth_key = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])
        try:
            data = auth_key.loads(token)
        except BadSignature:
            return False
        return data


class Note(db.Model):
    __tablename__ = "Notes"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(140), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Note %r>' % self.title

if __name__ == "__main__":
    db.create_all()