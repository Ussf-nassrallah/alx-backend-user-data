#!/usr/bin/env python3
''' auth module '''

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    ''' Auth class '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' require_auth method '''
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[len(path) - 1] != '/':
            path += '/'

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        ''' authorization_header method '''
        header_auth = request.headers.get('Authorization')
        if request is None or header_auth is None:
            return None
        return header_auth

    def current_user(self, request=None) -> TypeVar('User'):
        ''' current_user method '''
        return None

    def session_cookie(self, request=None):
        ''' returns a cookie value from a request '''
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        cookie = request.cookies.get(session_name)
        return cookie
