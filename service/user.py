import hashlib

from constans import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:

    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_user_by_username(self, username):
        return self.dao.get_user_by_username(username)

    def create(self, user_d):
        user_pass = user_d.get('password')
        user_hashed_pass = self.get_hash(user_pass)
        user_d['password'] = user_hashed_pass
        return self.dao.create(user_d)

    def update(self, user_d):
        user_pass = user_d.get('password')
        user_hashed_pass = self.get_hash(user_pass)
        user_d['password'] = user_hashed_pass
        return self.dao.update(user_d)

    def delete(self, uid):
        return self.dao.delete(uid)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")
