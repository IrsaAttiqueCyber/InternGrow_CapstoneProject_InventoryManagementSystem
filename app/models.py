from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(200),
        nullable=False
    )

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )


class Product(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    price = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    def __repr__(self):

        return f"<Product {self.name}>"