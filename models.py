from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/flask_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
flask_bcrypt = Bcrypt(app)

user_product = db.Table('orders',     # For association between Users, Products
    db.Column('user_id', db.Integer(), db.ForeignKey('Users.user_id')),
    db.Column('product_id', db.Integer(), db.ForeignKey('Products.product_id')))

class Users(db.Model,UserMixin):  # Table to store users details
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer(), primary_key=True)
    user_mail = db.Column(db.String(30), nullable=False, unique=True)
    user_name = db.Column(db.String(25), nullable=False, unique=True)
    user_paswd = db.Column(db.String(200),nullable=False, unique=True)
    #product_id = db.Column(db.Integer(), db.ForeignKey('Products.product_id'),nullable=False)
    products = db.relationship('Products', secondary=user_product, backref=db.backref('ref_user'))
    def get_id(self):
           return (self.user_id)

    
class Products(db.Model, UserMixin):   # Table to store products details
    __tablename__ = 'Products'
    product_id = db.Column(db.Integer(), primary_key=True)
    #user_id = db.Column(db.Integer(), db.ForeignKey('Users.user_id'),nullable=False)
    product_name = db.Column(db.String(30), nullable=False, unique=True)
    product_cost = db.Column(db.Integer(), nullable=False)
    product_desc = db.Column(db.String(300), nullable=False)
    