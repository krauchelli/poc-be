from flask import request, jsonify, Flask
from flask_jwt_extended import jwt_required, get_jwt_identity
import bcrypt
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

@jwt_required()
def GetUserById(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # validate if user_id is not the same as the current user
        if current_user_id != user_id:
            return jsonify({
                "statusCode": 403,
                "message": "Forbidden Access"
            }), 403
        
        user = models["get_user_by_id"](user_id)
        # validate if user is not exist
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

        # hash password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        user = {
            "email": email,
            "username": username,
            "password": hashed_password.decode("utf-8")
        }

        created_user = models["create_user"](user)
        return jsonify({
            "statusCode": 201,
            "message": "User created successfully",
            "data": created_user
        }), 201
    except Exception as e:
        return handle_exception(e)

@jwt_required()
def UpdateUser(user_id):
    try:
        req_body = request.json
        username = req_body.get("username")
        newPassword = req_body.get("password")
        phoneNumber = req_body.get("phoneNumber")
        exist_user = models["get_user_by_id"](user_id)
        current_user_id = get_jwt_identity()

        # validate if user is not exist
        if not exist_user:
            return jsonify({
                "statusCode": 404,
                "message": f"User with ID: {user_id} not found"
            }), 404
        # validate if one of them is empty, keep the old value
        if not username: 
            username = exist_user["username"]
        if not phoneNumber:
            phoneNumber = exist_user["phoneNumber"]
        if newPassword:
            # hash password
            hashed_password = bcrypt.hashpw(newPassword.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        else:
            hashed_password = exist_user["password"]


        user = {
            "username": username,
            "password": hashed_password,
            "phoneNumber": phoneNumber,
            "updatedBy": current_user_id
        }

        updated_user = models["update_user"](user_id, user)
        return jsonify({
            "statusCode": 200,
            "message": "User updated successfully",
            "data": updated_user
        }), 200
    except Exception as e:
        return handle_exception(e)

@jwt_required()
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
    
# will be replacing DeleteUser
@jwt_required()
def SoftDeleteUser(user_id):
    try:
        exist_user = models["get_user_by_id"](user_id)
        # validate
        if not exist_user:
            return jsonify({
                "statusCode": 404,
                "message": f"User with ID: {user_id} not found"
            }), 404
        if exist_user["status"] == "DELETED":
            return jsonify({
                "statusCode": 400,
                "message": f"User with ID: {user_id} already deleted"
            }), 400

        deleted_user = models["soft_delete_user"](user_id)

        return jsonify({
            "statusCode": 200,
            "message": "User deleted successfully",
            "data": deleted_user
        }), 200
    except Exception as e:
        return handle_exception(e)