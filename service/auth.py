import jwt
from flask import request
from flask_restx import abort

from constans import SECRET, ALGO


class AuthService:

    def admin_required(self, func):
        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                abort(401)

            data = request.headers['Authorization']
            token = data.split("Bearer ")[-1]
            try:
                user = jwt.decode(token, SECRET, algorithms=[ALGO])
                role = user.get("role")
            except Exception as e:
                print("JWT Decode Exception", e)
                abort(401)
            if role != "admin":
                abort(403)
            return func(*args, **kwargs)

        return wrapper

    def auth_required(self, func):
        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                abort(401)

            data = request.headers['Authorization']
            token = data.split("Bearer ")[-1]
            try:
                jwt.decode(token, SECRET, algorithms=[ALGO])
            except Exception as e:
                print(f"Traceback: {e}")
                abort(401)
            return func(*args, **kwargs)

        return wrapper
