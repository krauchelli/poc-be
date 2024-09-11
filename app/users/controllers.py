from flask import request, jsonify, Flask

from app.users.models import models

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({
        "statusCode": 500,
        "message": str(e)
    }), 500


def GetAllUsers():
    users = models["get_all_users"]()
    try: 
        return jsonify({
            "statusCode": 200,
            "message": "Success",
            "data": users
        }), 200
    except Exception as e:
        return handle_exception(e)


def GetUserById(user_id):
    try:
        user = models["get_user_by_id"](user_id)

        #validate
        if not user:
            return jsonify({
                "statusCode": 404,
                "message": f"User with ID: {user_id} not found"
            }), 404

        return jsonify({
            "statusCode": 200,
            "message": "Success",
            "data": user
        }), 200
    except Exception as e:
        return handle_exception(e)


def CreateUser():
    try:
        req_body = request.json
        email = req_body.get("email")
        username = req_body.get("username")
        password = req_body.get("password")

        # validate if one of them is empty
        if not email or not username or not password:
            return jsonify({
                "statusCode": 400,
                "message": "Email, username, and password are required"
            }), 400
        # validate if email is already exist
        exist_user_email = models["get_user_by_email"](email)
        if exist_user_email:
            return jsonify({
                "statusCode": 400,
                "message": "Email is already exist"
            }), 400
        # validate if username is already exist
        exist_user_username = models["get_user_by_username"](username)
        if exist_user_username:
            return jsonify({
                "statusCode": 400,
                "message": "Username is already exist"
            }), 400


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
    except Exception as e:
        return handle_exception(e)


def UpdateUser(user_id):
    try:
        req_body = request.json
        username = req_body.get("username")
        password = req_body.get("password")
        exist_user = models["get_user_by_id"](user_id)

        # validate if user is not exist
        if not exist_user:
            return jsonify({
                "statusCode": 404,
                "message": f"User with ID: {user_id} not found"
            }), 404
        # validate if one of them is empty, keep the old value
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
    except Exception as e:
        return handle_exception(e)


def DeleteUser(user_id):
    try:
        exist_user = models["get_user_by_id"](user_id)
        # validate
        if not exist_user:
            return jsonify({
                "statusCode": 404,
                "message": f"User with ID: {user_id} not found"
            }), 404
        
        deleted_user = models["delete_user"](user_id)

        return jsonify({
            "statusCode": 200,
            "message": "User deleted successfully",
            "data": deleted_user
        }), 200
    except Exception as e:
        return handle_exception(e)