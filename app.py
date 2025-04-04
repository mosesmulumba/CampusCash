from flask import Flask 
from resources.extensions import db, jwt, session , mail
from routes import *
from resources.resources import api , auth_ns , student_ns , savings_ns , loans_ns , projects_ns
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

# configurng the sql instance
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://campuscashuser:CampusCash-2025@localhost/campuscash" #mysql+pmysql://username:password@localhost/your_db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# configuring the jwt
app.config["JWT_SECRET_KEY"] = "mosesmulumba@94"

# configuring the sessins
app.config["SESSION_TYPE"] = "filesystem"

# configuring the flask-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'mulumbamoses94@gmail.com'
app.config['MAIL_PASSWORD'] = 'ivci jbij vkaz odoz'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail.init_app(app)

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})


api.init_app(app)

db.init_app(app)
session.init_app(app)
jwt.init_app(app)

migrate = Migrate(app , db)


api.add_namespace(auth_ns)
api.add_namespace(student_ns)
api.add_namespace(savings_ns)
api.add_namespace(withdrawal_ns)
api.add_namespace(loans_ns)
api.add_namespace(projects_ns)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

