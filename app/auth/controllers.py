from flask import request, jsonify, Flask
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import bcrypt
from app.auth.services import create_jwt_token, add_token_to_blacklist
from app.users.models import models

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({
        "statusCode": 500,
        "message": str(e)
    }), 500


def Register():
    try:
        req_body = request.json
        email = req_body.get("email")
        username = req_body.get("username")
        password = req_body.get("password")
        # default system for user registration
        systemName = "SYSTEM"

        # validate if email, username, or password is empty
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
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = {
            "email": email,
            "username": username,
            "password": hashed_password.decode('utf-8'),
            "createdBy": systemName,
            "updatedBy": systemName
        }
        created_user = models["create_user"](user)

        return jsonify({
            "statusCode": 201,
            "message": "User created successfully",
            "data": created_user
        }), 201
    except Exception as e:
        return handle_exception(e)


def Login():
    try:
        req_body = request.json
        email = req_body.get("email")
        password = req_body.get("password")

        # validate if email or password is empty
        if not email or not password:
            return jsonify({
                "statusCode": 400,
                "message": "Email and password are required"
            }), 400
        # validate if user is not exist
        exist_user = models["get_user_by_email"](email)
        if not exist_user:
            return jsonify({
                "statusCode": 404,
                "message": "User not found"
            }), 404
        # validate password
        if not bcrypt.checkpw(password.encode('utf-8'), exist_user["password"].encode('utf-8')):
            return jsonify({
                "statusCode": 400,
                "message": "Password is incorrect"
            }), 400
        
        # jwt token
        access_token = create_jwt_token(exist_user["id"])

        return jsonify({
            "statusCode": 200,
            "message": "Login successfully",
            "data": exist_user,
            "access_token": access_token
        }), 200
    except Exception as e:
        return handle_exception(e)

@jwt_required()
def Logout():
    try:
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()  # Extract user identity from the JWT

        # validate that the user ID is not None
        if not user_id:
            return jsonify({
                "statusCode": 400,
                "message": "User ID missing in the JWT"
            }), 400

        # Add token to blacklist
        add_token_to_blacklist(jti, user_id)

        return jsonify({
            "statusCode": 200,
            "message": "Logout successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "statusCode": 500,
            "message": f"Internal Server Error: {str(e)}"
        }), 500
    