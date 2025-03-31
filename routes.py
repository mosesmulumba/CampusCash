from flask import jsonify , request , abort
from datetime import datetime
from flask_jwt_extended import create_access_token , jwt_required , get_jwt_identity
from flask_restx import Resource
from resources.extensions import db , jwt , session
from resources.resources import auth_ns
from api_models import *
from models import *

@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.doc('signin to the platform' , description="Login to the Campus Cash platform with your username and password.") 
    @auth_ns.expect(login_model)
    def post(self):

        d = request.json

        student = Student.query.filter_by(username=d['username']).first()

        if student and student.password == d['password']:

            access_token = create_access_token(identity={'student_id':student.student_id})
            
            student_data = student.to_dict()

            student_data[access_token] = access_token

            return jsonify(student_data)

        
        return {'msg': 'Bad Username or email'} , 401
    
@student_ns.route("")
class Student_LIST_API(Resource):
    @student_ns.doc('get the students' , description="Retrieve all the students' record")
    @student_ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()
    
    @student_ns.doc('add new student details' , description="Add a new student to the campus cash platform")
    @student_ns.expect(student_input_model)
    @student_ns.marshal_list_with(student_model)
    def post(self):

        data_payload = student_ns.payload

        if not Student.is_valid_student_university_email(data_payload['student_email']):
            abort(400 , "Invalid student email format, Use a student university email with @stud.umu.ac.ug")


        new_student = Student(
            username = data_payload['username'],
            student_email = data_payload['student_email'],
            password = data_payload['password'],
            phone_number = data_payload['phone_number'],
            )

        db.session.add(new_student)
        db.session.commit()
        return new_student , 201
    

@student_ns.route("/<int:student_id>")
class Student_ByID(Resource):
    @student_ns.doc('get student by their id' , description="Retrieve all the student details for the student")
    @student_ns.marshal_list_with(student_model)
    def get(self, student_id):
        student = Student.query.get(student_id)
        return student
    
    @student_ns.doc('update the student details' , description="Retrieve all the student's details and update the specific details")
    @student_ns.expect(student_input_model)
    @student_ns.marshal_with(student_model)
    def put(self , student_id):

        new_student = Student.query.get(student_id)

        if not new_student:
            return {'msg': 'Student not found'}
        
        st = student_ns.payload


        new_student.username = st.get('username', new_student.username)
        new_student.student_email = st.get('student_email', new_student.student_email)
        new_student.password = st.get('password', new_student.password)
        new_student.phone_number = st.get('phone_number', new_student.phone_number)
        new_student.savings = st.get('savings', new_student.savings)
        
        if isinstance(new_student.savings, dict):
            new_student.savings = list(new_student.savings.values())  # Convert dict to list if needed

        new_student.loans = st.get('loans', new_student.loans)
        new_student.projects = st.get('projects', new_student.projects)

        db.session.commit()
        return new_student
    
    def delete(self , student_id):
        student = Student.query.get(student_id)
        db.session.delete(student)
        db.session.commit()
        return {'msg' : 'Student with id {student_id} has been successfully deleted.'} , 204


@savings_ns.route("")
class Savings_LIST_API(Resource):
    @savings_ns.doc('get_savings' , description="Retrieve all the savings record")
    @savings_ns.marshal_list_with(savings_model)
    def get(self):
        return Savings.query.all()

@savings_ns.route("/<int:id>")
class SavingDetailAPI(Resource):
    @savings_ns.doc('get_saving_by_id' , description="Retrieve a savings record by id")
    @savings_ns.marshal_list_with(savings_model)
    def get(self, id):

        saving = Savings.query.get(id)

        if not saving:
            abort(404 , "Saving details are not found")
        return saving

@savings_ns.route("/deposit")
class DepositAPI(Resource):
    @savings_ns.doc('depoist_money' , description="Deposi money into savings")
    @savings_ns.expect(savings_input_model)
    @savings_ns.marshal_with(savings_model)
    def post(self):

        data = request.json

        student = Student.query.get(data['student_id'])

        if not student:
            abort(404 , "Student not found")

        new_saving = Savings.deposit(
            student_id = data['student_id'],
            amount = data['amount'],
            balance = data['balance']
        )

        db.session.add(new_saving)
        db.session.commit()
        return new_saving


@savings_ns.route("/withdraw")
class WithdrawAPI(Resource):
    @savings_ns.doc('withdraw_request', description="Request a withdraw")
    @savings_ns.expect(savings_input_model)
    @savings_ns.marshal_with(savings_model)
    def post(self):

        data = request.json
        current_user = get_jwt_identity()
        savings = Savings.query.filter_by(student_id = current_user).first()

        if not savings:
            abort(404 , "Student not found")

        success , message = savings.request_withdrawal(data['amount'])

        if not success:
            abort(404 , "Insufficient funds")

        return {'message' : message} , 201


@savings_ns.route('/approve_withdraw/<int:id>')
class ApproveWithdrawalAPI(Resource):
    @savings_ns.doc('approve_withdrawal', description="Approve a withdrawal by the admin user")
    @jwt_required()
    def put(self , id):
        
        withdrawal = Savings.query.get(id)
    
        if not withdrawal:
            abort(404 , "Withdrawal request not found")
        
        succcess , message = withdrawal.approve_withdrawal(admin_user = get_jwt_identity())

        if not succcess:
            abort(404, message)

        return {'message' : message}, 200 


@loans_ns.route("")
class Loans_LIST_API(Resource):
    @loans_ns.doc("get all the loan details" , description="Fetch all the available loans")
    @loans_ns.marshal_list_with(loans_model)
    def get(self):
        return Loans.query.all()
    

@loans_ns.route("/<int:id>")
class LoanDetails(Resource):
    @loans_ns.doc("get the single loan details" , description="Fetch the details for a single loan")
    @loans_ns.marshal_list_with(loans_model)
    def get(self, id):
        loan = Loans.query.get(id)

        if not loan:
            abort(404 , "Loan details not found")

        return loan
    

    def delete(self , id):

        loan = Loans.query.get(id)

        if not loan:
            abort(404 , "The loan details are not found")


        db.session.delete(loan)
        db.session.commit()
        return {'msg' : 'The loan with id {id} has been successfully deleted.'} , 201
    

@loans_ns.route("/apply")
class Apply_For_A_loan(Resource):
    @loans_ns.doc("apply for a loan" , description="Apply for a loan")
    @loans_ns.expect(loans_input_model)
    @loans_ns.marshal_with(loans_model)
    def post(self):

        loan_data = request.json

        student = Student.query.get(loan_data['student_id'])

        if not student:
            abort(404, "Loan not there in the system")

        new_loan = Loans(
            student_id = loan_data['student_id'],
            amount = loan_data['amount'],
            collateral = loan_data['collateral'],
            status = loan_data['status'],
            repayment_deadline = loan_data['repayment_deadline']
        )

        db.session.add(new_loan)
        db.session.commit()
        return new_loan
    

@loans_ns.route("/approve/<int:id>")
class Approve_Loan(Resource):
    @loans_ns.doc("approve the selected loan" , description="Approve the selected loan by the admin at the Campus-Cash")
    @loans_ns.expect(loans_input_model)
    @loans_ns.marshal_with(loans_model)
    def put(self , id):

        loan = Loans.query.get(id)

        if not loan:
            abort(404 , "The loan details are not there!")

        loan_payload = loans_ns.payload

        loan.student_id = loan_payload.get('student_id' , loan.student_id)
        loan.amount = loan_payload.get('amount' , loan.amount)
        loan.collateral = loan_payload.get('collateral' , loan.collateral)
        loan.status = loan_payload.get('status' , loan.status)
        loan.repayment_deadline = loan_payload.get('repayment_deadline' , loan.repayment_deadline)


        db.session.commit()
        return loan

@projects_ns.route("")
class Projects_LIST_API(Resource):
    @projects_ns.doc("get all the projects" , description="Fetch all the presented projects with their details") 
    @projects_ns.marshal_list_with(projects_model)
    def get(self):

        projects = Projects.query.all()

        if not projects:
            abort(404 , "There are no projects presented so far!")

        return projects
    
@projects_ns.route("/add_project")
class Project_Request_Funding(Resource):
    @projects_ns.doc("create project to be funded", description="Submit project for funding.")
    @projects_ns.expect(project_input_model)
    @projects_ns.marshal_with(projects_model)
    def post(self):

        project_data = request.json

        student = Student.query.get(project_data['user_id'])

        if not student:
            abort(404 , "Student details not found")

        
        new_project = Projects(
            user_id = project_data['user_id'],
            title = project_data['title'],
            description = project_data['description'],
            requested_funds = project_data['requested_funds'],
            status = project_data['status'],
        )


        db.session.add(new_project)
        db.session.commit()
        return new_project
    
    

@projects_ns.route("/<int:id>")
class ProjectsDetails(Resource):
    @projects_ns.doc("get the details for a single project" , description="Fetch the details for a single project.")
    @projects_ns.marshal_with(projects_model)
    def get(self , id):

        project = Projects.query.get(id)

        if not project:
            abort(404, "Project details not found")
        
        return project
    
    @projects_ns.doc("delete the project with the id")
    def delete(self, id):

        project = Projects.query.get(id)

        db.session.delete(project)
        db.session.commit()
        return {'msg': "Project with {id} has been deleted successfully!"}
    
    @projects_ns.doc("update the project with id" , description="Update the project with the id")
    @projects_ns.expect(project_input_model)
    @projects_ns.marshal_with(projects_model)
    def put(self, id):

        project = Projects.query.get(id)

        if not project:
            abort(404 , "The project details are not found")

        project_payload = projects_ns.payload

        project.user_id = project_payload.get('user_id' , project.user_id),
        project.title = project_payload.get('title' , project.title),
        project.description = project_payload.get('description' , project.description),
        project.requested_funds = project_payload.get('requested_funds' , project.requested_funds),
        project.status = project_payload.get('status' , project.status)

        db.session.commit()
        return project



@projects_ns.route("/approve_project/<int:id>")
class AprroveProject(Resource):
    @projects_ns.doc("approve the project by admin" , description="Approve the submitted project by admin")
    @projects_ns.expect(project_input_model)
    @projects_ns.marshal_with(projects_model)
    def put(self, id):

        project = Projects.query.get(id)

        if not project:
            abort(404 , "The project details are not found")

        project_payload = projects_ns.payload

        project.user_id = project_payload.get('user_id' , project.user_id),
        project.title = project_payload.get('title' , project.title),
        project.description = project_payload.get('description' , project.description),
        project.requested_funds = project_payload.get('requested_funds' , project.requested_funds),
        project.status = project_payload.get('status' , project.status)

        db.session.commit()
        return project

    