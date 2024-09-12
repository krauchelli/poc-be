import jwt
import datetime
from prisma import Prisma
from prisma.models import TokenBlacklist
from flask_jwt_extended import create_access_token

prisma = Prisma()

def create_jwt_token(user_id):
    expiration = datetime.timedelta(hours=1)
    access_token = create_access_token(identity=user_id, expires_delta=expiration)
    return access_token

def add_token_to_blacklist(jti, user_id):
    # JTI stands for JWT ID. It is a unique identifier for the token.

    blacklist_token = TokenBlacklist.prisma().create(
        data={
            'jti': jti,
            'userId': user_id,
        }
    )

    return blacklist_token.dict()

def is_token_blacklisted(jti):
    blacklisted_token = TokenBlacklist.prisma().find_unique(where={"jti": jti})
    return blacklisted_token is not None