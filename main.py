from flask import Flask, request, redirect, render_template, jsonify, make_response
from security import token_required, secret_key, encrypted_data
import datetime
import jwt
import common_function as cf
import pandas as pd
from user import User

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home/index.html')


@app.route("/login")
def login():
    auth = request.authorization
    if auth and auth.password == "password":
        user = User(encrypted_data(auth.username), encrypted_data(auth.password))
        cf.get_save_file(1, user.toJson())
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=60)}, secret_key)
        return f'<a href="http://localhost:5000/get_system_list?token={token}">Private link</a>'
    return make_response('Could not Verify', 401, {'WWW-Authenticate': 'Basic realm ="Login Required"'})


@app.route("/get_system_list")
@token_required
def get_system_list():
    data = cf.get_save_file(1)
    df = pd.read_json(data)
    print(df)
    return jsonify({'message': 'valid jwt token'})


if __name__ == '__main__':
    app.run()

