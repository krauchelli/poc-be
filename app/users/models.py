from prisma import Prisma
from prisma.models import User
import uuid
from datetime import datetime
from time import time

prisma = Prisma()

def get_all_users():
    #users = User.prisma().find_many()
    users = User.prisma().find_many(where={"status": "ACTIVE"})
    return [user.dict() for user in users]

def get_user_by_id(user_id: uuid.UUID):
    start_time = time()
    user = User.prisma().find_unique(where={"id": str(user_id), "status": "ACTIVE"})
    end_time = time()
    print(f"Execution time: {end_time - start_time}")
    return user.dict() if user else None

def get_user_by_email(email: str):
    user = User.prisma().find_unique(where={"email": email, "status": "ACTIVE"})
    return user.dict() if user else None

def get_user_by_username(username: str):
    user = User.prisma().find_unique(where={"username": username, "status": "ACTIVE"})
    return user.dict() if user else None

def create_user(user: dict):
    created_user = User.prisma().create(data=user)
    return created_user.dict()

def update_user(user_id: uuid.UUID, user: dict):
    updated_user = User.prisma().update(
        where={
            "id": str(user_id),
            "status": "ACTIVE"
        }, data=user)
    return updated_user.dict()

def delete_user(user_id: uuid.UUID):
    deleted_user = User.prisma().delete(where={"id": str(user_id)})
    return deleted_user.dict()

def soft_delete_user(user_id: uuid.UUID):
    deleted_user = User.prisma().update(where={"id": str(user_id)}, data={
        "status": "DELETED",
        "deletedAt": str(datetime.now().astimezone().isoformat())
    })
    return deleted_user.dict()

models = {
    "get_all_users": get_all_users,
    "get_user_by_id": get_user_by_id,
    "get_user_by_email": get_user_by_email,
    "get_user_by_username": get_user_by_username,
    "create_user": create_user,
    "update_user": update_user,
    "delete_user": delete_user,
    "soft_delete_user": soft_delete_user
}