from flask import abort, Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

from todo_api.extensions import login_manager
from todo_api.models import DatabaseError, User, TodoItem, validate_id


blueprint = Blueprint('routes', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

@blueprint.route('/login', methods=['POST'])
def do_login():
    login_info = request.get_json()
    try:
        login = login_info['login']
        password = login_info['password']
    except KeyError:
        abort(400, 'JSON missing "login" or "password" key')

    try:
        user = User.find_user(login)
    except DatabaseError as e:
        abort(500, str(e))

    if user is not None and password == user.password:
        login_user(user)
        return '', 204
    else:
        abort(401, 'Incorrect username or password')

@blueprint.route('/todo/todo_items', methods=['POST'])
@login_required
def create_todo_item():
    if not request.json:
        abort(400, 'No JSON in request')

    todo = request.get_json()
    if 'title' not in todo:
        abort(400, 'JSON missing required "title" key')
    else:
        try:
            item = TodoItem.create(
                user_id=current_user.id,
                title=todo['title'],
                description=todo.get('description', ''),
                completed=False,
            )
        except DatabaseError as e:
            abort(500, str(e))

        return jsonify(item.jsonify()), 201

@blueprint.route('/todo/todo_items/<string:item_id>', methods=['PUT'])
@login_required
def update_todo_item(item_id):
    if not request.json:
        abort(400, 'No JSON in request')

    if not validate_id(item_id):
        abort(400, 'Todo item id: %s is not a valid id' % item_id)

    try:
        item = TodoItem.find_item(item_id)
    except DatabaseError as e:
        abort(500, str(e))

    if item is None:
        abort(404, 'Todo item with id: %s not found' % item_id)

    updated_todo = request.get_json()
    if 'completed' not in updated_todo:
        abort(400, 'JSON missing required "completed" key')
    else:
        try:
            item.update(completed=updated_todo['completed'])
        except DatabaseError as e:
            abort(500, str(e))
        else:
            return jsonify(item.jsonify()), 200

@blueprint.route('/todo/todo_items/<string:user_id>', methods=['GET'])
@login_required
def get_user_todo_items(user_id):
    if not validate_id(user_id):
        abort(400, 'Todo user id: %s is not a valid id' % user_id)

    try:
        items = TodoItem.find_user_items(user_id)
    except DatabaseError as e:
        abort(500, str(e))

    return jsonify([item.jsonify() for item in items]), 200

@blueprint.route('/todo/todo_items/<string:item_id>', methods=['DELETE'])
@login_required
def delete_todo_item(item_id):
    if not validate_id(item_id):
        abort(400, 'Todo item id: %s is not a valid id' % item_id)

    try:
        TodoItem.delete_item(item_id)
    except DatabaseError as e:
        abort(500, str(e))
    else:
        return '', 204

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return '', 200
