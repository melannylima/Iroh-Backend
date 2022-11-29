import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')

# CREATE
@user.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()

    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "A user that with name already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        login_user(user)
        print(f"{current_user.username} is current_user.username is POST register")

        user_dict = model_to_dict(user)
        del user_dict['password']

        return jsonify(
            data = user_dict,
            message = 'Success',
            code = 201
        ), 201

# LOGIN
@user.route('/login', methods=['POST'])
def login():
    payload = request.get_json()

    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)

        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print (user, 'is user')
            return jsonify(
                data = user_dict,
                message = 'Success',
                code = 200
            ), 200
        else:
            return jsonify(
                data = {},
                message = 'Username or Password is invalid.',
                code = 401
            ), 401
    except models.DoesNotExist:
        return jsonify(
            data = {},
            message = 'Username or Password is incorrect',
            code = 401
        ), 401


# LOG OUT
@user.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(
        data = {},
        message = 'Successfully logged out.',
        code = 200
    ), 200


# LOGGED IN?
@user.route('/logged_in', methods=['GET'])
def get_logged_in_user():
    print(current_user.username)
    user_dict = model_to_dict(current_user)
    user_dict.pop('password')
    return jsonify(
        data = user_dict,
        code = 200
    ), 200