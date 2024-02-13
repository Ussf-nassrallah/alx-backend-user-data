#!/usr/bin/env python3
''' basic_auth module '''
from api.v1.auth.auth import Auth
import base64
import binascii
import re
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    ''' BasicAuth class '''
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        ''' extract_base64_authorization_header method '''
        if authorization_header is None\
                or not isinstance(authorization_header, str)\
                or authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        ''' decode_base64_authorization_header method '''
        if base64_authorization_header is None\
                or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_hdr_auth = base64.b64decode(
                base64_authorization_header,
                validate=True
            )
            return decoded_hdr_auth.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str,
    ) -> Tuple[str, str]:
        ''' decoded value of a Base64 string '''
        if isinstance(decoded_base64_authorization_header, str):
            user_info = r'(?P<user>[^:]+):(?P<password>.+)'

            fields = re.fullmatch(
                user_info,
                decoded_base64_authorization_header.strip(),
            )

            if fields is not None:
                user = fields.group('user')
                password = fields.group('password')
                return (user, password)

        return None, None

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        ''' user_object_from_credentials method '''
        if user_email is None or user_pwd is None:
            return None
        try:
            users_list = User.search({'email': user_email})
        except Exception:
            return None
        if len(users_list) <= 0:
            return None
        if users_list[0].is_valid_password(user_pwd):
            return users_list[0]
