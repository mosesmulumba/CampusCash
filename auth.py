from flask import request 
from flask_restful import Resource
from .resources.extensions import db , session
from .models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Register(Resource):
    def post(self):
        data = request.json
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        new_user = User(name=data["name"], email=data["student_email"], password=data["password"])
        db.session.add(new_user)
        db.session.commit()
        return {"message":"User registered successful"}
    

class Login(Resource):
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data["student_email"]).first()
        if user and bcrypt.check_password_hash(user.password, data["password"]):
            session["user_id"] = user.id
            return {"message":"Login successful"}
        return {"message" : "Invalid login credentials"}


class Logout(Resource):
    def post(self):
        session.pop("user_id", None)
        return {"message" : "Logged out successfully"}
    

