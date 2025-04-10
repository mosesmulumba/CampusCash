from flask_restx import abort
from resources.extensions import db
from flask_bcrypt import Bcrypt
from datetime import timedelta , datetime
from flask_jwt_extended import create_access_token , jwt_required , get_jwt_identity
from flask_login import UserMixin
import re

bcrypt = Bcrypt()

class Student(db.Model , UserMixin):
    student_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100) , nullable=False)
    student_email = db.Column(db.String(100) , nullable=False)
    password = db.Column(db.String(100) , nullable=False)
    phone_number = db.Column(db.String(15) , nullable=False)
    is_admin = db.Column(db.Boolean , default=False)
    created_date = db.Column(db.DateTime , default = db.func.current_timestamp())

    def __init__(self , username , student_email , password , phone_number , is_admin):
        self.username = username
        self.student_email = student_email
        self.password = password
        self.phone_number = phone_number
        self.is_admin = is_admin

    # @staticmethod
    def is_valid_student_university_email(student_email):
        pattern = r'^[a-zA-Z0-9,.%+-]+@stud\.umu\.ac\.ug$'
        return re.match(pattern , student_email) is not None
    
    # student_email = "mulumba.moses@stud.umu.ac.ug"

    
    def password_is_vlaid(self, password):
        return bcrypt.check_password_hash(self.password , password)
    
    def generate_access_token(self , student):
        expiry = timedelta(days=1)
        return create_access_token(student , expires_delta=expiry)
    

    def to_dict(self):
        return {
            "student_id" : self.student_id,
            "username" : self.username,
            "student_email" : self.student_email,
            "password" : self.password,
            "is_Admin" : self.is_admin,
            "phone_number" : self.phone_number,
            "created_date" : self.created_date.strftime('%Y-%m-%dT%H:%M:%S') if isinstance(self.created_date, datetime) else self.created_date,
            "loans": [loan.to_dict() for loan in self.loans],
            "savings": [saving.to_dict() for saving in self.savings],
            "projects" : [project.to_dict() for project in self.projects],
            "withdrawals": [withdrawal.to_dict() for withdrawal in self.withdrawals],
        }    
    
class Savings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), default="pending") 
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    student = db.relationship('Student', backref='savings')

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "amount": self.amount,
            "balance": self.balance, 
            "status" : self.status,
            "created_date": self.created_date.strftime('%Y-%m-%dT%H:%M:%S') if isinstance(self.created_date, datetime) else self.created_date
        }

    def deposit(self, amount):
        self.amount = amount
        self.balance += amount  # Update balance
        self.status = 'deposited'
        db.session.commit()




class Loans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer , db.ForeignKey('student.student_id') , nullable=False)
    savings_id = db.Column(db.Integer , db.ForeignKey('savings.id') , nullable=False)
    amount = db.Column(db.Float , nullable=False)
    collateral = db.Column(db.Float , nullable=False)
    status = db.Column(db.String(15) , default='pending')
    interest_rate = db.Column(db.Float , default=0.10)
    penalty_rate = db.Column(db.Float , default=0.05)
    repayment_deadline = db.Column(db.Date , nullable=False)
    created_date = db.Column(db.DateTime , default=db.func.current_timestamp())

    student = db.relationship('Student' , backref='loans')
    savings = db.relationship('Savings' , backref=db.backref('loans' , lazy=True))

    def to_dict(self):
        return {
        "id" : self.id,
        "student_id" : self.student_id,
        "savings_id" : self.savings_id,
        "amount" : self.amount,
        "collateral" : self.collateral,
        "status" : self.status,
        "interest_rate" : self.interest_rate,
        "penalty_rate" : self.penalty_rate,
        "repayment_deadline" : self.repayment_deadline,
        "created_date" : self.created_date
        }

    def validate_loan(self):

        pending_withdrawals = Withdrawals.query.filter_by(student_id=self.student_id , status='pending').first()

        if pending_withdrawals:
            return abort(400 , "You have a pending withdrawal so you can't apply for a loan.") , 400
        
        savings = Savings.query.filter_by(student_id=self.student_id).first()

        collateral_balance = savings.balance

        if collateral_balance is None:
            return {'msg' : "Your savings balance is not set. Please contact support team."} , 400


        if self.amount > (collateral_balance * 5):
            return {"Not elligible to get a loan"} , 403
        
        existing_loans = Loans.query.filter(
            (Loans.student_id == self.student_id) & 
            (Loans.status == 'pending')
            ).first()
        

        if existing_loans:
            return False, "User already has an active loan"
        return True, "Loan meets approval criteria"
    
    def approve_loan(self):

        if self.status == 'pending':
            self.status = "approved"
            self.repayment_deadline = datetime.now() + timedelta(days=10)
            db.session.commit()
            return True, "Loan approved successfully"
        
        self.status = "not approved"
        return False , "Loan not approved"
    

    def reject_loan(self):

        if self.status == 'pending':
            self.status = 'rejected'
            db.session.commit()
            return True , "Loan rejected successfully"
        
        self.status = 'not rejected'
        return False, "Loan not rejected"
    
    
    def calculate_penalty(self):
        if self.status == "approved" and self.repayment_deadline and datetime.now() > self.repayment_deadline:
            overdue_time = ((datetime.now() - self.repayment_deadline).days) // 7
            return self.amount * (self.penalty_rate * overdue_time)
        return 0


class Withdrawals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), default="pending") 
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    student = db.relationship('Student', backref='withdrawals')

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "amount": self.amount,
            "balance": self.balance, 
            "status" : self.status,
            "created_date": self.created_date.strftime('%Y-%m-%dT%H:%M:%S') if isinstance(self.created_date, datetime) else self.created_date
        }


    def approve(self):
        if self.status != "pending":
            return False, "This request has already been processed"
        
        savings = Savings.query.filter_by(student_id=self.student_id).first()
        
        if not savings:
            return False, "No savings record found"

        if self.amount > savings.balance:
            return False, "Insufficient funds"

        savings.balance -= self.amount  # Deduct from balance
        self.status = "approved"  # Mark as approved
        db.session.commit()
        return True, "Withdrawal approved"
    
    def reject_withdrawal(self):

        savings = Savings.query.filter_by(student_id=self.student_id).first()
        print(f"{savings.balance}")

        withdrawal = Withdrawals.query.filter_by(student_id=self.student_id).first()
        print(f"{withdrawal.balance}")
        
        if self.status == 'pending':
            savings.balance = withdrawal.balance
            self.status = 'rejected'
            db.session.commit()
            return True, "Withdrawal rejected"
        
        self.status = 'not rejected'
        return False, "Rejected withdrawal"




class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey('student.student_id') , nullable=False)
    title = db.Column(db.String(100) , nullable=False)
    description = db.Column(db.Text , nullable=False)
    requested_funds = db.Column(db.Float , nullable=False)
    status = db.Column(db.String(15) , default='pending')
    created_date = db.Column(db.DateTime , default=db.func.current_timestamp())

    student = db.relationship('Student' , backref='projects')

    def to_dict(self):
        return {
        "id" : self.id,
        "user_id" : self.user_id,
        "title" : self.title,
        "description" : self.description,
        "requested_funds" : self.requested_funds,
        "status" : self.status,
        "created_date" : self.created_date,
        }
        

    def approve_project(self):
        """ Admin approves project funding. """
        # Ensure the SACCO has enough funds
        total_savings = db.session.query(db.func.sum(Savings.balance)).scalar() or 0
        if self.requested_funds > total_savings:
            self.status = "rejected"
            return False, "Project rejected."
        self.status = "approved"
        db.session.commit()
        return True, "Project approved for funding."
    
    def reject_project(self):
        if self.status == 'pending':
            self.status = 'rejected'
            return True, "project rejected"
        
        self.status = 'not rejected'
        return False, "Project rejected"
    



class Notifications(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    message = db.Column(db.String(255) , nullable=False)
    is_read = db.Column(db.Boolean , default=False , nullable=False)
    timestamp = db.Column(db.DateTime , default=datetime.now)
    student_id = db.Column(db.Integer , db.ForeignKey('student.student_id') , nullable=False)
    project_id = db.Column(db.Integer , db.ForeignKey('projects.id') , nullable=False)
    loan_id = db.Column(db.Integer , db.ForeignKey('loans.id') , nullable=False)
    withdrawal_id = db.Column(db.Integer , db.ForeignKey('withdrawals.id') , nullable=False)

    student = db.relationship('Student' , backref='notifications')
    loan = db.relationship('Loans' , backref='notifications')
    withdrawal = db.relationship('Withdrawals' , backref='notifications')
    project = db.relationship('Projects' , backref='notifications')




    def to_dict(self):
        return {
        "id" : self.id,
        "message" : self.message,
        "student_id" : self.student_id,
        "is_read" : self.is_read,
        "timestamp" : self.timestamp,
        }
