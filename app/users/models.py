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

def update_user(user_id: uuid.UUID, user: dict):
    updated_user = User.prisma().update(where={"id": str(user_id)}, data=user)
    return updated_user.dict()

def delete_user(user_id: uuid.UUID):
    deleted_user = User.prisma().delete(where={"id": str(user_id)})
    return deleted_user.dict()

models = {
    "get_all_users": get_all_users,
    "get_user_by_id": get_user_by_id,
    "create_user": create_user,
    "update_user": update_user,
    "delete_user": delete_user
}