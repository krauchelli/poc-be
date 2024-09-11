from flask import Blueprint, jsonify, request
from manager import app
from .controllers import GetAllUsers, CreateUser

users_controllers = Blueprint('users', __name__)

@users_controllers.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return GetAllUsers()
    if request.method == 'POST':
        return CreateUser()