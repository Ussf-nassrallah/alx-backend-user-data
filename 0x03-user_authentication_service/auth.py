#!/usr/bin/env python3
''' auth module '''

import bcrypt


def _hash_password(password: str) -> bytes:
    ''' hash user password '''
    user_pssw = password.encode('utf-8')
    encoded_user_pssw = bcrypt.hashpw(user_pssw, bcrypt.gensalt())
    return encoded_user_pssw
