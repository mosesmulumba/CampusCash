from flask_restful import Resource
from flask import request 
from resources.extensions import Session , db
from app.models import Savings

class Deposit(Resource):
    def post(self):
        if "user_id" not in Session:
            return {"message": "Unauthorized !!"} , 401
        data = request.json
        new_savings = Savings(user_id = Session["user_id"], amount=data["amount"], transaction_type="deposit")
        db.Session.add(new_savings)
        db.Session.commit()
        return {"message" : "Deposit successful"} , 201
