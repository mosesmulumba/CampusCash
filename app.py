from flask import Flask 
from resources.extensions import db, jwt, session
from routes import *
from resources.resources import api , auth_ns , student_ns , savings_ns , loans_ns , projects_ns
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://campuscashuser:CampusCash-2025@localhost/campuscash" #mysql+pmysql://username:password@localhost/your_db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "mosesmulumba@94"
app.config["SESSION_TYPE"] = "filesystem"

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})


api.init_app(app)
db.init_app(app)
session.init_app(app)
jwt.init_app(app)

migrate = Migrate(app , db)


api.add_namespace(auth_ns)
api.add_namespace(student_ns)
api.add_namespace(savings_ns)
api.add_namespace(loans_ns)
api.add_namespace(projects_ns)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

