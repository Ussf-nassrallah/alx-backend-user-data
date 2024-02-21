#!/usr/bin/env python3
''' auth module '''

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    ''' hash user password '''
    user_pssw = password.encode('utf-8')
    encoded_user_pssw = bcrypt.hashpw(user_pssw, bcrypt.gensalt())
    return encoded_user_pssw


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' register a new user '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pssd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pssd)
            return new_user
        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        ''' handle user login '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        # get password from exists user
        hash_user_passw = user.hashed_password
        # encode user password that come from user req
        encoded_user_passw = password.encode('utf-8')
        # is_valid should can be True or False
        is_valid = bcrypt.checkpw(encoded_user_passw, hash_user_passw)
        return is_valid
