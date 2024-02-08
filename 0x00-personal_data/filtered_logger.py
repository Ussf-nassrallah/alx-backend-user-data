#!/usr/bin/env python3
''' filtered_logger module '''

import os
import logging
import re
from typing import List
import mysql.connector

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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """get_db method thats connect with mysql database"""

    username = os.getenv("PERSONAL_DATA_DB_USERNAME") or "root"
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD") or ""
    host = os.getenv("PERSONAL_DATA_DB_HOST") or "localhost"
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connect = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return connect


def main():
    '''Main entry point for logging user data'''

    database = get_db()
    logger_instance = get_logger()
    db_cursor = database.cursor()
    db_cursor.execute("SELECT * FROM users;")
    column_names = db_cursor.column_names

    for row_data in db_cursor:
        mssg = "".join(f"{k}={v}; " for k, v in zip(column_names, row_data))
        logger_instance.info(mssg.strip())

    db_cursor.close()
    database.close()


if __name__ == "__main__":
    main()
