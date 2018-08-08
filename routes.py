import json

from flask import abort, Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_pymongo import ObjectId

from extensions import login_manager
from models import User, TodoItem
from util import jsonify_item


blueprint = Blueprint('routes', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

@blueprint.route('/login', methods=['POST'])
def login():
    login_info = request.get_json()
    try:
        login = login_info['login']
        password = login_info['password']
    except KeyError:
        abort(400, 'JSON missing "login" or "password" key')

    try:
        user = User.objects(login=login_info['login']).first()
    except Exception:
        abort(500, 'Database error')

    if user is not None and login_info['password'] == user.password:
        login_user(user)
        return '', 204
    else:
        abort(401, 'Incorrect username or password')

@blueprint.route('/todo_items', methods=['POST'])
@login_required
def create_todo_item():
    if not request.json:
        abort(400, 'No JSON in request')

    todo = request.get_json()
    if 'title' not in todo:
        abort(400, 'JSON missing required "title" key')
    else:
        try:
            item = TodoItem(
                user_id=current_user.id,
                title=todo['title'],
                description=todo.get('description', ''),
                completed=False,
            ).save()
        except Exception:
            abort(500, 'Database error')

        return jsonify(jsonify_item(item)), 201

@blueprint.route('/todo_items/<string:item_id>', methods=['PUT'])
@login_required
def update_todo_item(item_id):
    if not request.json:
        abort(400, 'No JSON in request')

    if not ObjectId.is_valid(item_id):
        abort(400, 'Todo item id: %s is not a valid id' % item_id)

    try:
        item = TodoItem.objects(id=item_id).first()
    except Exception:
        abort(500, 'Database error')

    if item is None:
        abort(404, 'Todo item with id: %s not found' % item_id)

    updated_todo = request.get_json()
    if 'completed' not in updated_todo:
        abort(400, 'JSON missing required "completed" key')
    else:
        item.completed = updated_todo['completed']
        item.save()
        return jsonify(jsonify_item(item)), 200

@blueprint.route('/todo_items/<string:user_id>', methods=['GET'])
@login_required
def get_user_todo_items(user_id):
    if not ObjectId.is_valid(user_id):
        abort(400, 'Todo user id: %s is not a valid id' % user_id)

    try:
        items = TodoItem.objects(user_id=user_id)
    except Exception:
        abort(500, 'Database error')

    return jsonify([jsonify_item(item) for item in items]), 200

@blueprint.route('/logout')
@login_required
def logout_view():
    logout_user()



