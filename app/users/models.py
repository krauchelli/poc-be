from prisma import Prisma

prisma = Prisma()

def get_all_users():
    return prisma.user.find_many()