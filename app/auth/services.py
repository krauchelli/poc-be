import jwt
import datetime
from flask_jwt_extended import create_access_token

def create_jwt_token(user_id):
    expiration = datetime.timedelta(hours=1)
    access_token = create_access_token(identity=user_id, expires_delta=expiration)
    return access_token