#!/usr/bin/env python3
''' session_auth module '''
from api.v1.auth.auth import Auth
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
