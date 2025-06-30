from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
swagger = Swagger()
migrate = Migrate()