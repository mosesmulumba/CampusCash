from .resources.extensions import db
from flask_bcrypt import Bcrypt
from datetime import timedelta , datetime
from flask_jwt_extended import create_access_token , jwt_required , get_jwt_identity
from flask_login import UserMixin
import re

bcrypt = Bcrypt()

class Student(db.Model,UserMixin):
    student_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100) , nullable=False)
    student_email = db.Column(db.String(100) , nullable=False)
    password = db.Column(db.String(100) , nullable=False)
    phone_number = db.Column(db.String(15) , nullable=False)
    created_date = db.Column(db.DateTime , default=db.func.current_timestamp())

    def __init__(self , username , student_email , password , phone_number):
        self.username = username
        self.student_email = student_email
        self.password = password
        self.phone_number = phone_number

    @staticmethod
    def is_valid_student_university_email(student_email):
        pattern = r'^[a-zA-Z0-9,_%+-]+@stud\.umu\.ac\.ug$'
        return re.match(pattern , student_email)
    
    # student_email = "mulumba.moses@stud.umu.ac.ug"

    # if is_valid_student_university_email(student_email):
    #     print("Valid student email, adding student to the student sacco system")
    # else:
    #     print("Invalid student email, please use the correct university email")

    
    def password_is_vlaid(self, password):
        return bcrypt.check_password_hash(self.password , password)
    
    def generate_access_token(self , student):
        expiry = timedelta(days=1)
        return create_access_token(student , expires_delta=expiry)
    



class Loans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer , db.ForeignKey('student.id') , nullable=False)
    amount = db.Column(db.Float , nullable=False)
    collateral = db.Column(db.Float , nullable=False)
    status = db.Column(db.String(15) , default='pending')
    interest_rate = db.Column(db.Float , default=0.10)
    penalty_rate = db.Column(db.Float , default=0.05)
    repayment_deadline = db.Column(db.Date , nullable=False)
    created_date = db.Column(db.DateTime , default=db.func.current_timestamp())

    student = db.relationship('Student' , backref='loans')

    def validate_loan(self):
        if self.amount > (self.collateral * 5):
            return False, "Not elligible to get a loan"
        existing_loans = Loans.query.filter_by(student_id= self.student_id, status="approved").count()

        if existing_loans > 0:
            return False, "User already has an active loan"
        return True, "Loan meets approval criteria"
    
    def approve_loan(self, admin_user):
        valid, message = self.validate_loan()
        if valid:
            self.status = "approved"
            self.repayment_deadline = datetime.now() + timedelta(days=90)
            db.session.commit()
            return True, "Loan approved successfully"
        return False , "Loan not approved"
    
    def calculate_penalty(self):
        if self.status == "approved" and self.repayment_deadline and datetime.now() > self.repayment_deadline:
            overdue_time = ((datetime.now() - self.repayment_deadline).days) // 7
            return self.amount * (self.penalty_rate * overdue_time)
        return 0
    

class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer , db.ForeignKey('student.id') , nullable=False)
    amount = db.Column(db.Float , nullable=False)
    status = db.Column(db.String(15) , default='pending')
    transaction_type = db.Column(db.String(20) , nullable=False)
    created_date = db.Column(db.DateTime , default=db.func.current_timestamp())

    student = db.relationship('Student' , backref='savings')


    def deposit(self , amount):
        self.amount += amount 
        self.status = "approved"
        db.session.commit()

    def request_withdrawal(self , amount):
        if amount > self.amount:
            return False,
        self.transaction_type = "withdrawal"
        self.status = "pending"
        db.session.commit()
        return True, "Withdrawal request submitted"

    def approve_withdrawal(self, admin_user):
        if self.status == "pending":
            self.status = "approved"
            self.amount -= self.amount
            db.session.commit()
            return True, "Withdrawal approved"
        return False, "No pending withdrawals"

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey('student.id') , nullable=False)
    title = db.Column(db.String(100) , nullable=False)
    description = db.Column(db.Text , nullable=False)
    requested_funds = db.Column(db.Float , nullable=False)
    status = db.Column(db.String(15) , default='pending')
    created_date = db.Column(db.DateTime , default=db.func.current_timestamp())

    student = db.relationship('Student' , backref='projects')
        

    def approve_project(self, admin_user):
        """ Admin approves project funding. """
        # Ensure the SACCO has enough funds
        total_savings = db.session.query(db.func.sum(Savings.amount)).scalar() or 0
        if self.requested_funds > total_savings:
            return False, "Not enough funds in SACCO."
        self.status = "approved"
        db.session.commit()
        return True, "Project approved for funding."

    def reject_project(self, admin_user):
        """ Admin rejects project funding. """
        self.status = "rejected"
        db.session.commit()
        return True, "Project rejected."


