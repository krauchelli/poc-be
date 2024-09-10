from flask import request, jsonify

from app.users.models import get_all_users

def GetAllUsers():
    users = get_all_users()
    return jsonify(users)