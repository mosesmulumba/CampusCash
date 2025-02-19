from .extensions import db 
from flask_restx import Api , Namespace

api = Api(version='1.1.0' , title="Campus Cash" , description="Students' SACCO System")

auth_ns = Namespace('auth' , description='authentication operations')
student_ns = Namespace('student' , description='student operations')
savings_ns = Namespace('savings' , description='savings operations')
loans_ns = Namespace('loans' , description='loans operations')
projects_ns = Namespace('projects' , description='projects operations')
