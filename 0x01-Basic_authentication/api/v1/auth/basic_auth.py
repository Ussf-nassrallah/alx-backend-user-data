#!/usr/bin/env python3
''' basic_auth module '''
from api.v1.auth.auth import Auth
import base64
import binascii


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
