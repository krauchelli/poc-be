from flask import Flask
from config import configs
from prisma import Prisma

def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(configs[config_mode])

    return app