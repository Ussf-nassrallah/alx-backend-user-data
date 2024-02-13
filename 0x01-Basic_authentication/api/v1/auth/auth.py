#!/usr/bin/env python3
''' auth module '''

from flask import request
from typing import List, TypeVar


class Auth():
    ''' Auth class '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' require_auth method '''
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for exc_path in excluded_paths:
            if exc_path == path\
                    or exc_path[:-1] == path or exc_path == path[:-1]:
                return False
            else:
                return True

    def authorization_header(self, request=None) -> str:
        ''' authorization_header method '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' current_user method '''
        return None