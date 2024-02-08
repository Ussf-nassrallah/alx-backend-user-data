#!/usr/bin/env python3
''' filtered_logger module '''

import re
from typing import List


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
