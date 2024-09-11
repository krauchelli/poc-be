import os
from app import create_app
from prisma import Prisma, register
from flask_jwt_extended import JWTManager

app = create_app(os.getenv('CONFIG_MODE'))

# jwt configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

#routes
# simple initial caller
@app.route('/<name>')
def index(name):
    return 'Hello, {}'.format(name)
#blueprints
from app.auth.urls import auth_controllers
from app.users.urls import users_controllers
app.register_blueprint(auth_controllers, url_prefix='/v1/auth')
app.register_blueprint(users_controllers, url_prefix='/v1/users')



# listener
if __name__ == '__main__':
    app.run(debug=True)