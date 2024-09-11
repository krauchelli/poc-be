from flask import Blueprint, jsonify, request
from manager import app
from .controllers import GetAllUsers, CreateUser, GetUserById, UpdateUser

users_controllers = Blueprint('users', __name__)

@users_controllers.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return GetAllUsers()
    if request.method == 'POST':
        return CreateUser()

@users_controllers.route('/users/<user_id>', methods=['GET', 'PUT'])
def user(user_id):
    if request.method == 'GET':
        return GetUserById(user_id)
    if request.method == 'PUT':
        return UpdateUser(user_id)