import os
from app import create_app
from prisma import Prisma, register

# db = Prisma()
# db.connect()
# register(db)

app = create_app(os.getenv('CONFIG_MODE'))

#routes
# simple initial caller
@app.route('/<name>')
def index(name):
    return 'Hello, {}'.format(name)
#blueprints
from app.users.urls import users_controllers
app.register_blueprint(users_controllers, url_prefix='/v1/users')


# listener
if __name__ == '__main__':
    app.run(debug=True)