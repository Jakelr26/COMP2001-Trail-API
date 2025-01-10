import json
import os
from cryptography.fernet import Fernet
from flask import jsonify
from functools import wraps

def role_req (*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            permissions_and_role = check_for_token()
            dataholder = json.loads(permissions_and_role)
            permissions = dataholder['role']
            print(permissions)
            if isinstance(permissions, str):
                permissions = permissions.split(",") # splitem in two is both there

            if not any(role in permissions for role in roles):
                return jsonify({'message' : 'You dont have the required permissions to access this endpoint'}), 403
            return f(*args, **kwargs)
        return wrapped
    return wrapper




def check_for_token():
    key = os.environ.get("key")
    if not key:
        print("Error: encryption key not found in environment variables.")
        return

    key = key.encode()
    cipher_suite = Fernet(key)

    try:
        with open("permissions.json", "r") as f:
            permissions = json.load(f)
            encrypted_permissions = permissions["role_token"]
    except FileNotFoundError:
        print("Error: permissions.json file not found.")
        return

    try:
        decrypted_permissions = cipher_suite.decrypt(encrypted_permissions.encode()).decode()
        print(decrypted_permissions)
    except Exception as e:
        print("Error during decrpty")
        print(e)
        return

    return decrypted_permissions


# All below is no longer needed, was to be part of JWTS

# def check_for_token(function):
#     @wraps(function)
#     def wrapped(*args, **kwargs):
# #------
#
#
#         token = request.args.get('token')
#         print(token)
#         if not token:
#             return jsonify({'message' : 'Token is missing!'}), 401
#         try:
#             data = jwt.decode(token, config.app.config['SECRET_KEY'], algorithms=["HS256"])
#         except:
#             return jsonify({'message': 'Invalid token'}), 403
#
#         return function(*args, **kwargs)
#     return wrapped



#======
# was for the webapp part
# token = request.cookies.get('token') #get token from login
# print("Request Headers:", dict(request.headers))
# auth = request.headers.get('Authorization')
#
#
#
# if not auth or not auth.startswith('Bearer '):
#     return jsonify({'message' : 'Token is missing!'}), 401
#
#
#
# try:
#     token = auth.split(' ')[1]  # pulls out the token from the long string thing
#     print("Extracted Token:", token)
#
#     data = jwt.decode(token, config.app.config['SECRET_KEY'], algorithms=["HS256"])
#     print("Token data:", data)
# except jwt.ExpiredSignatureError:
#     return jsonify({'message' : 'Token has expired!, session has finished, Re-login to continue :)'}), 401
# except jwt.InvalidTokenError:
#     return jsonify({'message' : 'Token is invalid! So you dont have permissions to be here :('}), 401
# except Exception as e:
#     print("Unexpected error:", e)
#     return jsonify({'message' : 'Token is invalid! So you dont have permissions to be here :('}), 401



#================
            # auth_header = request.headers.get('Authorization')
            # if not auth_header or not auth_header.startswith('Bearer '):
            #     return jsonify({'message' : 'Token is missing!'}), 403
            # token = auth_header.split(' ')[1]
            # print("Request Headers:", dict(request.headers))
            # auth = request.headers.get('Authorization')
            # print("Authorization Header:", auth)
            #
            # try:
            #     data = jwt.decode(token, config.app.config['SECRET_KEY'], algorithms=["HS256"])
            #     print("Token data:", data)
            # except jwt.ExpiredSignatureError:
            #     return jsonify({'message' : 'Token has expired!, session has finished, Re-login to continue :)'}), 403
            # except jwt.InvalidTokenError:
            #     return jsonify({'message' : 'Token is invalid! So you dont have permissions to be here :('}), 403
            # if data['role'] not in roles:
    #         #     return jsonify({'message' : 'You dont have the required permissions to access this endpoint'}), 403
    #
    #         return f(*args, **kwargs)
    #     return wrapped
    # return wrapper