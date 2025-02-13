from flask_restful import Resource
from flask import request 
from .extensions import session , db
from ..models import Savings

class Deposit(Resource):
    def post(self):
        if "user_id" not in session:
            return {"message": "Unauthorized !!"} , 401
        data = request.json
        new_savings = Savings(user_id = session["user_id"], amount=data["amount"], transaction_type="deposit")
        db.session.add(new_savings)
        db.session.commit()
        return {"message" : "Deposit successful"} , 201
