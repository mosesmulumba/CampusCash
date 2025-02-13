from flask import Flask
from flask_restful import Api
from .resources.extensions import db , session , jwt
from .config.config import Config
from .auth import Register , Login , Logout
from .resources.savings import Deposit
from flasgger import Swagger
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def home():
    return "Hello, Flask is working!"

db.init_app(app)
session.init_app(app)
jwt.init_app(app)

migrate = Migrate(app , db)

# swagger
app.config['SWAGGER'] = {
    'title': 'Campus Cash API',
    'uiversion': 1
    }


Swagger(app, template_file='api_docs.yml')

api = Api(app)

api.add_resource(Register , "/auth/register")
api.add_resource(Login , "/auth/login")
api.add_resource(Logout , "/auth/logout")
api.add_resource(Deposit , "/savings/deposit")


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

