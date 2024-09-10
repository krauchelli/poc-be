from flask import Blueprint, jsonify, request
from manager import app
from .controllers import GetAllUsers

users_controllers = Blueprint('users', __name__)

@users_controllers.route('/users', methods=['GET'])
def users():
    return GetAllUsers()