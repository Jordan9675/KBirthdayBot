from datetime import datetime
from typing import Tuple

import pytz
import requests
from bs4 import BeautifulSoup
from requests.models import Response

from .utils import convert_expression_to_hashtag

def get_seoul_current_date() -> Tuple[str, str]:
    seoul_timezone = pytz.timezone("Asia/Seoul")
    current_datetime = datetime.now(seoul_timezone)

    return str(current_datetime.month), str(current_datetime.day)


BIRTHDAY_URL = "https://dbkpop.com/db/k-pop-birthdays"
MONTH, DAY = get_seoul_current_date()


class Birthday:

    @staticmethod
    def request_url(url: str) -> Response:
        """Perform a GET request."""
        return requests.get(url)

    @staticmethod
    def convert_response_to_soup(response: Response) -> BeautifulSoup:
        """Convert a GET request response to soup."""
        return BeautifulSoup(response.text, "html.parser")

    @staticmethod
    def _locate_birthday_table(soup: BeautifulSoup) -> BeautifulSoup:
        return soup.select_one("#table_1")

    @staticmethod
    def _locate_rows_from_birthday_table(table: BeautifulSoup) -> BeautifulSoup:
        return table.select("tbody > tr")

    @staticmethod
    def _get_column_values(row: BeautifulSoup) -> list:
        return row.find_all("td")

    @staticmethod
    def _parse_column_values(column_values: list) -> dict:
        return {
            "groupName": column_values[1].text,
            "idolName": column_values[2].text,
            "birthYear": column_values[4].text,
            "birthMonth": column_values[5].text,
            "birthDay": column_values[6].text,
            "age": column_values[7].text,
            "gender": column_values[8].text
        }

    @staticmethod
    def _birthday_matches_day_and_month(birthday: dict) -> bool:
        """Check whether a given birthday matches today's date."""
        return birthday["birthMonth"] == MONTH and birthday["birthDay"] == DAY

    @staticmethod
    def get_todays_birthdays() -> list:
        birthdays = Birthday.get_birthdays()

        return [birthday for birthday in birthdays if
                Birthday._birthday_matches_day_and_month(birthday)]

    @staticmethod
    def get_birthdays() -> list:
        """Retrieving data about upcoming idols' birthdays."""
        response = Birthday.request_url(BIRTHDAY_URL)
        soup = Birthday.convert_response_to_soup(response)
        table = Birthday._locate_birthday_table(soup)
        rows = Birthday._locate_rows_from_birthday_table(table)
        columns_values = [Birthday._get_column_values(row) for row in rows]
        return [Birthday._parse_column_values(
            columns_value) for columns_value in columns_values]

    def generate_birthday_message(birthday: dict) -> str:
        return f"Happy {birthday['idolName']} day ! \U0001F973\U0001F382\n\n" \
            f"{convert_expression_to_hashtag(birthday['idolName'])} " \
            f"{convert_expression_to_hashtag(birthday['groupName'])} " \
            f"{convert_expression_to_hashtag('Kpop')} " \
            f"{convert_expression_to_hashtag('Birthday')}"


if __name__ == "__main__":
    print(DAY, MONTH)
    today = Birthday.get_todays_birthdays()
    print(today)
    for ppl in today:
        print(Birthday.generate_birthday_message(ppl))
        print("\n-------------------")
