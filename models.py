from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(20), nullable=False) # 'Ingreso' or 'Gasto'

    def __repr__(self):
        return f'<Category {self.name}>'

class Minister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_salary = db.Column(db.Numeric(10, 2), default=0.0)
    housing_allowance = db.Column(db.Numeric(10, 2), default=0.0)

    def __repr__(self):
        return f'<Minister {self.name}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('transactions', lazy=True))

    # Optional link to a minister if this transaction is a payment to one
    minister_id = db.Column(db.Integer, db.ForeignKey('minister.id'), nullable=True)
    minister = db.relationship('Minister', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f'<Transaction {self.description} - {self.amount}>'
