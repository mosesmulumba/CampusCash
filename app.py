from flask import Flask
from flask_restx import Api
from resources.extensions import *
from resources.resources import *
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://campuscashuser:CampusCash-2025@localhost/campuscash" #mysql+pmysql://username:password@localhost/your_db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "mosesmulumba@94"
app.config["SESSION_TYPE"] = "filesystem"

api.init_app(app)

api.add_namespace(auth_ns)
api.add_namespace(student_ns)
api.add_namespace(savings_ns)
api.add_namespace(loans_ns)
api.add_namespace(projects_ns)


db.init_app(app)
session.init_app(app)
jwt.init_app(app)

migrate = Migrate(app)

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

