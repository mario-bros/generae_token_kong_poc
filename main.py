from flask import jsonify, request, Flask
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    JWTManager
)

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401

users = [
    {'id': 1, 'username': 'Taro', 'email': 'taro@email.com', 'password': 'taro'},
    {'id': 2, 'username': 'Hanako', 'email': 'hanako@email.com', 'password': 'hanako'}
]


def jwt_unauthorized_loader_handler(reason):
    return jsonify({'message': 'Unauthorized'}), HTTP_UNAUTHORIZED


app = Flask(__name__)
app.url_map.strict_slashes = False

# Set up Flask-JWT-Extended extention
app.config['JWT_SECRET_KEY'] = 'talend'


jwt = JWTManager(app)
jwt.unauthorized_loader(jwt_unauthorized_loader_handler)

@jwt.additional_headers_loader
def custom_headers(identity):
    return {
        'iss': 'talend',
        # 'x-extra-header': 'extra-value'  # Example of another custom header
    }


@app.route('/api/login', methods=['POST'])
def login():
    if not request.is_json:
        body = {'message': 'Missing JSON in request'}
        return jsonify(body), HTTP_BAD_REQUEST

    request_body = request.get_json()
    if request_body is None:
        body = {'message': 'Request body is empty'}
        return jsonify(body), HTTP_BAD_REQUEST

    whitelist = {'email', 'password'}
    if not request_body.keys() <= whitelist:
        body = {'message': 'Missing email or password in request'}
        return jsonify(body), HTTP_BAD_REQUEST

    auth_user = None
    for user in users:
        isMatchEmail = user['email'] == request_body['email']
        isMatchPassword = user['password'] == request_body['password']
        if isMatchEmail and isMatchPassword:
            auth_user = user
            break

    if auth_user is None:
        body = {'message': 'Login failure. Bad email or password'}
        return jsonify(body), HTTP_UNAUTHORIZED

    # token = create_access_token(identity=auth_user['username'], additional_headers=)
    # token = create_access_token(identity=auth_user['username'])
    token = create_access_token(identity=auth_user['message'])
    body = {'message': 'Login succeeded', 'token': token}
    return jsonify(body), HTTP_OK


@app.route('/api/djp', methods=['GET'])
def index():
    return jsonify({'users': users}), HTTP_OK


if __name__ == '__main__':
    app.run()