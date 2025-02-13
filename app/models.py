from resources.extensions import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100) , nullable=False)
    student_email = db.Column(db.String(100) , nullable=False)
    password = db.Column(db.String(100) , nullable=False)
    phone_number = db.Column(db.String(15) , nullable=False)
    role = db.Column(db.String(10) , default='student')
    created_date = db.Column(db.DateTime , default=db.func.current_timestamp())


class Loans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable=False)
    amount = db.Column(db.Float , nullable=False)
    collateral = db.Column(db.Float , nullable=False)
    status = db.Column(db.String(15) , default='pending')
    repayment_deadline = db.Column(db.Date , nullable=False)
    created_date = db.Column(db.DateTime , default=db.func.current_timestamp())

    user = db.relationship('User' , backref='loans')
    

class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable=False)
    amount = db.Column(db.Float , nullable=False)
    transaction_type = db.Column(db.String(20) , nullable=False)
    created_date = db.Column(db.DateTime , default=db.func.current_timestamp())

    user = db.relationship('User' , backref='savings')


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable=False)
    title = db.Column(db.String(100) , nullable=False)
    description = db.Column(db.Text , nullable=False)
    requested_funds = db.Column(db.Float , nullable=False)
    status = db.Column(db.String(15) , default='pending')
    created_date = db.Column(db.DateTime , default=db.func.current_timestamp())

    user = db.relationship('User' , backref='projects')
        



