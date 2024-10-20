import json
from flask import Flask, request, redirect, render_template, jsonify, make_response
from security import token_required, secret_key, encrypted_data
import datetime
import jwt
import common_function as cf
import pandas as pd
from user import User
import hashlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('home/index.html')


@app.route("/create_login")
def create_login():
    auth = request.authorization
    if auth and auth.password == "password":
        pwd = hashlib.md5(auth.password.encode("utf-8")).hexdigest()
        user = User(auth.username, pwd)
        cf.get_save_file(1, user.toJson())
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=60)}, secret_key)
        return f'<a href="http://localhost:5000/get_system_list?token={token}">Private link</a>'
    return make_response('Could not Verify', 401, {'WWW-Authenticate': 'Basic realm ="Login Required"'})


# @app.route("/login", methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data['username']
#     password = data['password']

#     filename = cf.get_save_file(1)
#     with open(filename, 'r') as file:
#         data = json.loads(json.load(file))
#         print(data)

#     user = User(data['name'], data['password'])
#     pwd = hashlib.md5(password.encode("utf-8")).hexdigest()
#     if str(username).lower() == user.name and pwd == user.password:
#         token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow(
#         ) + datetime.timedelta(seconds=60)}, secret_key)
#         return f'{secret_key}'

@app.route("/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                'status': 'fail',
                'message': 'Username and password are required',
                'data': None
            }), 400

        filename = cf.get_save_file(1)
        with open(filename, 'r') as file:
            file_data = json.loads(json.load(file))

        user = User(file_data['name'], file_data['password'])
        hashed_password = hashlib.md5(password.encode("utf-8")).hexdigest()

        if str(username).lower() == user.name and hashed_password == user.password:
            token = jwt.encode({
                'user': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
            }, secret_key)

            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'data': {'token': token}
            }), 200
        else:
            return jsonify({
                'status': 'fail',
                'message': 'Invalid username or password',
                'data': None
            }), 401

    except FileNotFoundError:
        return jsonify({
            'status': 'error',
            'message': 'User data file not found',
            'data': None
        }), 500

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': None
        }), 500

@app.route("/change_password", methods=['GET', 'POST'])
# @token_required
def change_password():
    password = request.args.get('password')
    pwd = hashlib.md5(password.encode("utf-8")).hexdigest()
    user = User('admin', pwd)
    cf.get_save_file(1, user.toJson())
    return make_response('Could not Verify', 401)


@app.route("/get_system_list", methods=['GET', 'POST'])
# @token_required
def get_system_list():
    data = cf.get_save_file(1)
    df = pd.read_json(data)
    print(df)
    return jsonify({'message': 'valid jwt token'})


if __name__ == '__main__':
    app.run()

