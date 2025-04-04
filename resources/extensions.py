from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_jwt_extended import JWTManager
from flask_mail import Mail


mail = Mail()
db = SQLAlchemy()
jwt = JWTManager()
session = Session()
