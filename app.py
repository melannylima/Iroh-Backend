from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

import os

from dotenv import load_dotenv

load_dotenv()

from resources.tea import tea
from resources.users import user

import models

DEBUG = True # development
PORT = os.environ.get("PORT")

app = Flask(__name__)

app.secret_key = os.environ.get("APP_SECRET")

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except:
        return None

CORS(tea, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(tea, url_prefix='/api/v1/tea')
app.register_blueprint(user, url_prefix='/api/v1/user')

# @app.route('/')
# def index():
#     return 'it\'s working'

@app.before_request
def before_request():
    print("Before request")
    models.DATABASE.connect()

@app.after_request
def after_request(response):
    print("After request")
    models.DATABASE.close()
    return response

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)