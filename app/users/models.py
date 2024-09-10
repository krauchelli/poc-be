from prisma import Prisma
from prisma.models import User

prisma = Prisma()

def get_all_users():
    return User.prisma().find_many()