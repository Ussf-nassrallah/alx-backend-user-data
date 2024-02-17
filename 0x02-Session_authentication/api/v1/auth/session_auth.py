#!/usr/bin/env python3
''' session_auth module '''
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    ''' SessionAuth class '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
        create_session
        -> method that creates a Session ID for a user_id
        '''
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' return user_id based on session_id '''
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        '''
        current_user
        method that returns a User instance based on a cookie value
        '''
        cookie = self.session_cookie(request)
        current_user_id = self.user_id_for_session_id(cookie)
        current_user = User.get(current_user_id)
        return current_user
