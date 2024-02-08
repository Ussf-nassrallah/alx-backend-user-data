#!/usr/bin/env python3
''' encrypt password module '''
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    ''' function thats hashed password '''
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pass


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' is_valid: function that checks if password is valid or not '''
    checked_pssw = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return checked_pssw
