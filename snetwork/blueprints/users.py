from flask import Blueprint, request, jsonify
from flask_login import login_user
from snetwork.models import User

users = Blueprint('users', __name__)


@users.route('user/login', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.username == username).first()
    if (not user or not password) or user.password != password:
        return jsonify({'status': 'error', 'data': None,
                        'message': 'Error trying to log in'})
    login_user(user)
    return jsonify({'status': 'sucesss', 'data': None,
                    'message': 'User has been logged in'})
