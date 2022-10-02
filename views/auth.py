from flask_restx import Resource, Namespace
from service.jwt_service import JwtService

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        jwt = JwtService()
        tokens = jwt.give_user_jwt_token()
        return tokens, 201

    def put(self):
        jwt = JwtService()
        tokens = jwt.check_refresh_token()
        return tokens, 201
