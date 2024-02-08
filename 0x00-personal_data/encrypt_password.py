#!/usr/bin/env python3
''' encrypt password module '''
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    ''' function thats hashed password '''
    encode_pssw = password.encode()
    hashed_pass = hashpw(b, bcrypt.gensalt())
    return hashed_pass


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' is_valid: function that checks if password is valid or not '''
    checked_pssw = bcrypt.checkpw(password.encode(), hashed_password)
    return checked_pssw
