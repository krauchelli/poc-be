from flask import Blueprint, jsonify, request
from manager import app
from .controllers import get_all_users

users_controllers = Blueprint('users', __name__)

@users_controllers.route('/users', methods=['GET'])
def users():
    return get_all_users()