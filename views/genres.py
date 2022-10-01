from flask import request
from flask_restx import Resource, Namespace

from utils import auth_required, admin_required
from dao.model.genre import GenreSchema
from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_data = request.json
        genre = genre_service.create(req_data)
        return genre.name, 200


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, gid):
        req_data = request.json
        if 'id' not in req_data:
            req_data["id"] = gid
        genre_service.update(req_data)
        return '', 204

    @admin_required
    def delete(self, gid):
        genre_service.delete(gid)
        return '', 204
