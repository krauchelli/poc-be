from flask import Blueprint, jsonify, request
from manager import app
from .controllers import GetAllUsers, CreateUser, GetUserById, UpdateUser, DeleteUser, SoftDeleteUser

users_controllers = Blueprint('users', __name__)

@users_controllers.route('', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return GetAllUsers()
    if request.method == 'POST':
        return CreateUser()

@users_controllers.route('<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        return GetUserById(user_id)
    if request.method == 'PUT':
        return UpdateUser(user_id)
    if request.method == 'DELETE':
        #return DeleteUser(user_id)
        return SoftDeleteUser(user_id)