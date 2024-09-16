import os
from app import create_app
from prisma import Prisma, register
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.auth.services import is_token_blacklisted

app = create_app(os.getenv('CONFIG_MODE'))

# cors
CORS(app, resources={r'/*': {'origins': '*'}}, max_age=86400)

# jwt configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# token blacklist check
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return is_token_blacklisted(jti)

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
    app.run(host="0.0.0.0", port=5000, threaded=True)