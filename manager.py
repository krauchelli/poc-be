import os
from app import create_app
from prisma import Prisma

db = Prisma()

app = create_app(os.getenv('CONFIG_MODE'))

@app.before_request
def before_request():
    print('test before request')
    db.connect()

@app.after_request
def after_request():
    print('test after request')
    db.disconnect()

#routes
# simple initial caller
@app.route('/<name>')
def index(name):
    return 'Hello, {}'.format(name)
#blueprints
from app.users.urls import users_controllers
app.register_blueprint(users_controllers)


# listener
if __name__ == '__main__':
    app.run()