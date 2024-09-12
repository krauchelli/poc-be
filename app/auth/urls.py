from flask import Blueprint, request
from app.auth.controllers import Register, Login, Logout

auth_controllers = Blueprint('auth', __name__)

@auth_controllers.route('/register', methods=['POST'])
def register():
    return Register()

@auth_controllers.route('/login', methods=['POST'])
def login():
    return Login()

@auth_controllers.route('/logout', methods=['POST'])
def logout():
    return Logout()