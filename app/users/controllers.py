from flask import request, jsonify

from app.users.models import models

def GetAllUsers():
    users = models["get_all_users"]()
    return jsonify({
        "statusCode": 200,
        "message": "Success",
        "data": users
    }), 200


def GetUserById(user_id):
    user = models["get_user_by_id"](user_id)
    return jsonify({
        "statusCode": 200,
        "message": "Success",
        "data": user
    }), 200


def CreateUser():
    req_body = request.json
    email = req_body.get("email")
    username = req_body.get("username")
    password = req_body.get("password")

    user = {
        "email": email,
        "username": username,
        "password": password
    }
    print(user)

    created_user = models["create_user"](user)
    return jsonify({
        "statusCode": 201,
        "message": "User created successfully",
        "data": created_user
    }), 201


def UpdateUser(user_id):
    req_body = request.json
    username = req_body.get("username")
    password = req_body.get("password")

    # validate if one of them is empty, keep the old value
    exist_user = models["get_user_by_id"](user_id)
    if not username: 
        username = exist_user["username"]
    if not password:
        password = exist_user["password"]

    user = {
        "username": username,
        "password": password
    }

    updated_user = models["update_user"](user_id, user)
    return jsonify({
        "statusCode": 200,
        "message": "User updated successfully",
        "data": updated_user
    }), 200