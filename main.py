import os
from flask import jsonify, request, Flask
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    JWTManager
)
import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_INTENAL_ERR = 500

users = [
    {'id': 1, 'username': 'bPJSTk', 'password': 'BPJSTKdev2024'},
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

    whitelist = {'username', 'password'}
    if not request_body.keys() <= whitelist:
        body = {'message': 'Missing username or password in request'}
        return jsonify(body), HTTP_BAD_REQUEST

    auth_user = None
    for user in users:
        isMatchUser = user['username'] == request_body['username']
        isMatchPassword = user['password'] == request_body['password']
        if isMatchUser and isMatchPassword:
            auth_user = user
            break

    if auth_user is None:
        body = {'message': 'Login failure. Bad email or password'}
        return jsonify(body), HTTP_UNAUTHORIZED

    token = create_access_token(identity=auth_user['username'])
    body = {'message': 'Login succeeded', 'token': token}
    return jsonify(body), HTTP_OK


@app.route('/api/djp', methods=['GET'])
def index():
    URL_DJP = os.getenv('URL_DJP')
    try:
        response = requests.get(URL_DJP)
        jsonResp = response.json()
        # jsonResp["data"]
        print(jsonResp)
        return jsonResp, HTTP_OK

        # response.raise_for_status()

        # token = create_access_token(identity=jsonResp["message"])
        # body = {'message': 'Login succeeded', 'token': token}
        # return jsonify(body), HTTP_OK

    except requests.exceptions.ConnectionError as ece:
        print("Connection Error:", ece)
        body = {'message': 'Connection Error'}
        return jsonify(body), HTTP_INTENAL_ERR
    except requests.exceptions.Timeout as et:
        print("Timeout Error:", et)
        body = {'message': 'Timeout Error'}
        return jsonify(body), HTTP_INTENAL_ERR
    except requests.exceptions.RequestException as e:
        print("Some Ambiguous Exception:", e)
        body = {'message': 'Some Ambiguous Exception'}
        return jsonify(body), HTTP_INTENAL_ERR
    
    # return jsonify({'users': users}), HTTP_OK


if __name__ == '__main__':
    app.run()