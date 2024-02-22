#!/usr/bin/env python3
''' auth module '''

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    ''' hash user password '''
    user_pssw = password.encode('utf-8')
    encoded_user_pssw = bcrypt.hashpw(user_pssw, bcrypt.gensalt())
    return encoded_user_pssw


def _generate_uuid() -> str:
    ''' generate uuid '''
    id = str(uuid.uuid4())
    return id


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

    def create_session(self, email: str) -> str:
        ''' create_session method '''
        try:
            # get user from DB
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # return None if user not exists
            return None
        sess_id = _generate_uuid()
        self._db.update_user(user.id, session_id=sess_id)
        return sess_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        ''' get user from session id '''
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        ''' destroy_session '''
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        ''' get reset password token '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token
