import json

from flask import Blueprint, request
from flask_login import login_required, login_user, logout_user

from extensions import login_manager
from models import User


blueprint = Blueprint('routes', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

@blueprint.route('/')
@login_required
def index():
    return "Hello World"

@blueprint.route('/login', methods=['POST'])
def login():
    login_info = request.get_json()
    try:
        login = login_info['login']
        password = login_info['password']
    except KeyError:
        return (
            json.dumps({'success': False}),
            400,
            {'ContentType': 'application/json'},
        )

    user = User.objects(login=login_info['login']).first()
    if user is not None and login_info['password'] == user.password:
        login_user(user)
        return (
            json.dumps({'success': True}),
            200,
            {'ContentType': 'application/json'},
        )
    else:
        return (
            json.dumps({'success': False}),
            401,
            {'ContentType': 'application/json'},
        )

@blueprint.route('/logout')
@login_required
def logout_view():
    logout_user()



