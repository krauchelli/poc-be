from flask import Flask
from config import configs
from prisma import Prisma, register

def create_app(config_mode):
    db = Prisma()
    db.connect()
    register(db)
    app = Flask(__name__)
    app.config.from_object(configs[config_mode])

    return app