import calendar
import datetime
import jwt

from flask import request, jsonify
from flask_restx import Resource, Namespace, abort

from constans import ALGO, SECRET
from implemented import user_service


auth_ns = Namespace('auth')

secret = 's3cR$eT'
algo = 'HS256'


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_data = request.json
        username = req_data.get('username', None)
        password = req_data.get('password', None)
        if None in [username, password]:
            return abort(401)

        user = user_service.get_user_by_username(username)
        if not user:
            return {"error": "Неверные учётные данные"}, 401

        user_pass = user_service.get_hash(password)
        if password != user_pass:
            return {"error": "Неверные учётные данные"}, 401

        data = {
            "username": user.username,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return jsonify(tokens), 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        try:
            data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        except Exception as e:
            abort(400)

        username = data.get("username")

        user = user_service.get_user_by_username(username)

        data = {
            "username": user.username,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201
