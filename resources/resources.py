from flask_restx import Api , Namespace

authorizations = {
    "BearerAuth" : {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}

api = Api(version='1.1.1' , title="Campus Cash" , description="Students' SACCO System" , authorizations=authorizations , security="BearerAuth")

auth_ns = Namespace('auth' , description="authentication operations")
student_ns = Namespace('students' , description='student operations')
savings_ns = Namespace('savings' , description='savings operations')
withdrawal_ns = Namespace('withdrawal', description='withdrawal operations')
loans_ns = Namespace('loans' , description='loans operations')
projects_ns = Namespace('projects' , description='projects operations')
