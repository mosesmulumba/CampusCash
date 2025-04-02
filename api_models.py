from flask_restx import fields
from resources.resources import *

login_model = auth_ns.model("LoginModel" , {
    "username" : fields.String(required=True),
    "password" : fields.String(required=True)
})


loans_model = loans_ns.model("LoansModel" , {
    "id" : fields.Integer(readOnly=True),
    "student_id" : fields.Integer(required=True),
    "savings_id" : fields.Integer(required=True),
    "amount" : fields.Float(required=True),
    "collateral" : fields.Float(required=True),
    "status" : fields.String(required=True),
    "repayment_deadline" : fields.DateTime(required=True),
    "created_date" : fields.DateTime(required=True)

})

loans_input_model = loans_ns.model("LoansInputModel" , {
    "student_id" : fields.Integer,
    "amount" : fields.Float,
    # "collateral" : fields.Float,
    # "status" : fields.String,
    "repayment_deadline" : fields.DateTime,
})

savings_model = savings_ns.model("SavingsModel" , {
    "id" : fields.Integer(readOnly=True),
    "student_id" : fields.Integer(required=True),
    "amount" : fields.Float(required=True),
    "balance" : fields.Float(required=True),
    "created_date" : fields.DateTime(required=True)
})

savings_input_model = savings_ns.model("SavingsInputModel" , {
    "student_id" : fields.Integer,
    "amount" : fields.Float,
})

withdrawal_model = withdrawal_ns.model("WithdrawalModel" ,{
    "id" : fields.Integer(readOnly=True),
    "student_id" : fields.Integer(required=True),
    "amount" : fields.Float(required=True),
    "balance" : fields.Float(required=True),
    "status" : fields.String(required=True),
    "created_date" : fields.DateTime(required=True) 
})

withdrawal_input_model = withdrawal_ns.model("WithdrwalInputModel",{
    "student_id" : fields.Integer,
    "amount" : fields.Float,
})
projects_model = projects_ns.model("ProjectsModel" , {
    "id" : fields.Integer(required=True),
    "user_id" : fields.Integer(required=True),
    "title" : fields.String(required=True),
    "description" : fields.String(required=True),
    "requested_funds" : fields.Float(required=True),
    "status" : fields.String(required=True),
    "created_date" : fields.DateTime(required=True)
})

project_input_model = projects_ns.model("ProjectsInputModel" , {
    "user_id" : fields.Integer,
    "title" : fields.String,
    "description" : fields.String,
    "requested_funds" : fields.Float,
    # "status" : fields.String
})

student_model = student_ns.model("StudentModel" , {
    "student_id" : fields.Integer,
    "username" : fields.String,
    "student_email" : fields.String,
    "password" : fields.String,
    "is_admin" : fields.Boolean,
    "phone_number": fields.String, 
    "created_date" : fields.DateTime,
    "savings" : fields.Nested(savings_model),
    "loans" : fields.Nested(loans_model),
    "projects" : fields.Nested(projects_model),
    "withdrawals" : fields.Nested(withdrawal_model)
})

student_input_model = student_ns.model("StudentInputModel" , {
    "username" : fields.String,
    "student_email" : fields.String,
    "password" : fields.String,
    "is_admin" : fields.Boolean,
    "phone_number": fields.String, 
    "savings" : fields.Nested(savings_model),
    "loans" : fields.Nested(loans_model),
    "projects" : fields.Nested(projects_model),
    "withdrawals" : fields.Nested(withdrawal_model)
})
