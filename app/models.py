from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import login_manager

db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(select(User).where(User.id == int(user_id)))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    posts = db.relationship(
                'Post',
                back_populates='user',
                lazy=True,
                cascade="all, delete-orphan"
            )

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_by_username(cls, username):
        return db.session.query(cls).filter(cls.username == username).first()

    def __repr__(self):
        return f'<User {self.id} {self.username!r}>'

class Post(db.Model):
    __tablename__    = 'posts'
    id               = db.Column(db.Integer, primary_key=True)
    created          = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    title            = db.Column(db.String(100), nullable=False)
    body             = db.Column(db.String(280), nullable=False)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_news_user_id'), nullable=False)
    parent_id = db.Column(db.Integer, unique=False, nullable=True)

    user = db.relationship(
                'User',
                back_populates='posts',
                lazy=True,
            )

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Article {self.id} {self.title!r}>'