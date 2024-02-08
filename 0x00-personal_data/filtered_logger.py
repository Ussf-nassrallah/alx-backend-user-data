#!/usr/bin/env python3
''' filtered_logger module '''

import logging
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    ''' filter_datum method that returns the log message obfuscated '''

    for field in fields:
        pattern = rf'{field}=.+?{separator}'
        message = re.sub(pattern, f'{field}={redaction}{separator}', message)

    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        ''' RedactingFormatter class constructor '''
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        ''' format method '''
        output = filter_datum(
            self.fields,
            self.REDACTION,
            super().format(record),
            self.SEPARATOR
        )
        return output


def get_logger() -> logging.Logger:
    ''' get_logger method '''
    user = logging.getLogger('user_data')
    user.setLevel(logging.INFO)
    user.propagate = False

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(PII_FIELDS))

    user.addHandler(streamHandler)

    return user
