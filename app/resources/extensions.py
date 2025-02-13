from flask_sqlalchemy import SQLAlchemy
from flask_session import session
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()
Session = session()
