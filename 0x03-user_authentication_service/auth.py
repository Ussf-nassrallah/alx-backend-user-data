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
