import os
import re
from datetime import datetime
from typing import Tuple

import pytz
import requests


def convert_expression_to_hashtag(expression: str) -> str:
    if expression.strip():
        return "#" + "".join(char for char in expression if char.isalnum()) + " "
    else:
        return ""


def remove_extra_space(text: str) -> str:
    return re.sub(r'\s+', ' ', text)


def get_seoul_current_date() -> Tuple[int, int]:
    seoul_timezone = pytz.timezone("Asia/Seoul")
    current_datetime = datetime.now(seoul_timezone)

    return current_datetime.month, current_datetime.day


def download_file_from_url(url: str, filename: str) -> None:
    response = requests.get(url)
    with open(filename, "wb") as file:
        file.write(response.content)


def delete_file(filepath: str) -> None:
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
