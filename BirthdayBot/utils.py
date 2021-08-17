from datetime import datetime
from typing import Tuple

import pytz


def convert_expression_to_hashtag(expression: str) -> str:
    if expression.strip():
        return "#" + "".join(char for char in expression if char.isalnum()) + " "
    else:
        return ""

def get_seoul_current_date() -> Tuple[int, int]:
    seoul_timezone = pytz.timezone("Asia/Seoul")
    current_datetime = datetime.now(seoul_timezone)

    return current_datetime.month, current_datetime.day

def get_current_date() -> Tuple[int, int]:
    current_datetime = datetime.now()
    
    return current_datetime.month, current_datetime.day