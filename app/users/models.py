from prisma import Prisma
from prisma.models import User
import uuid

prisma = Prisma()

def get_all_users():
    users = User.prisma().find_many()
    return [user.dict() for user in users]

def get_user_by_id(user_id: uuid.UUID):
    user = User.prisma().find_unique(where={"id": str(user_id)})
    return user.dict() if user else None

def create_user(user: dict):
    created_user = User.prisma().create(data=user)
    return created_user.dict()

models = {
    "get_all_users": get_all_users,
    "get_user_by_id": get_user_by_id,
    "create_user": create_user
}