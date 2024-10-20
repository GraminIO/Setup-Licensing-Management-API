import jwt
from flask import request, jsonify
from cryptography.fernet import Fernet


secret_key = "m5JnE2yuulmnZo-QemOghj6saEE_u4WTt3g-DFSTRlk="
# secret_key = Fernet.generate_key()
# print(secret_key)
cipher = Fernet(secret_key)


def token_required(f):
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            jwt.decode(token, secret_key, algorithms="HS256")
        except Exception as error:
            return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)
    return decorated


def encrypted_data(data):
    return cipher.encrypt(data.encode())


def decrypted_data(data):
    return cipher.decrypt(encrypted_data).decode()

