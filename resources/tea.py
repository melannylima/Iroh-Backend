import models 

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required

tea = Blueprint('tea', 'tea')

# INDEX
@tea.route('/', methods=['GET'])
def tea_index():

    result = models.Tea.select()
   
    tea_dicts = []
    for tea in result:
        tea_dict = model_to_dict(tea)
        tea_dicts.append(tea_dict)
        tea_dict['creator'].pop('password')

    return jsonify(
        data = tea_dicts,
        message = f"Found {len(tea_dicts)} tea recipes",
        status = 200
    ), 200

# MY INDEX
@tea.route('/il-mio', methods=['GET'])
def my_index():
    tea_dicts = [model_to_dict(tea) for tea in current_user.tea]

    for tea_dict in tea_dicts:
        tea_dict['creator'].pop('password')

    return jsonify(
        data = tea_dicts,
        message = f"Found {len(tea_dicts)} tea recipes",
        status = 200
    ), 200

# CREATE
@tea.route('/', methods=['POST'])
def create_tea():
    payload = request.get_json()
    print(payload)
    print(current_user.username)
    new_tea = models.Tea.create(name=payload['name'], recipe=payload['recipe'], brew_time=payload['brew_time'], creator=current_user.id, has_dairy=payload['has_dairy'], has_caffeine=payload['has_caffeine'], serve_iced=payload['serve_iced'])
    print(new_tea)

    tea_dict = model_to_dict(new_tea)
    tea_dict['creator'].pop('password')

    return jsonify(
        data = tea_dict,
        message = 'Created new tea recipe!',
        status = 201
    ), 201

# SHOW
@tea.route('/<id>', methods=['GET'])
def show_one_tea_recipe(id):
    tea = models.Tea.get_by_id(id)
    print(tea)

    tea_dict = model_to_dict(tea)
    tea_dict['creator'].pop('password')

    return jsonify(
        data = tea_dict,
        message = 'I see something...',
        status = 200
    ), 200

# UPDATE
@tea.route('/<id>', methods=['PUT'])
@login_required
def update_tea(id):
    payload = request.get_json()

    query = models.Tea.update(**payload).where(models.Tea.id == id)
    query.execute()

    return jsonify(
        data = model_to_dict(models.Tea.get_by_id(id)),
        status = 200,
        message = 'Tea recipe updated'
    ), 200

# DELETE
@tea.route('/<id>', methods=['DELETE'])
@login_required
def delete_tea(id):
    query = models.Tea.delete().where(models.Tea.id == id)
    query.execute()

    return jsonify(
        data = 'tea recipe deleted',
        message = 'tea recipe deleted',
        status = 200
    ), 200