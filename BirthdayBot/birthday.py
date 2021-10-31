import requests
from bs4 import BeautifulSoup
from requests.models import Response

from .utils import convert_expression_to_hashtag, get_seoul_current_date

BIRTHDAY_URL = "https://dbkpop.com/db/k-pop-birthdays"
seoul_current_month, seoul_current_day = get_seoul_current_date()


def request_url(url: str) -> Response:
    """Perform a GET request."""
    return requests.get(url)


def convert_response_to_soup(response: Response) -> BeautifulSoup:
    """Convert a GET request response to soup."""
    return BeautifulSoup(response.text, "html.parser")


def locate_birthday_tables(soup: BeautifulSoup) -> BeautifulSoup:
    return soup.select("#table_3, #table_1")


def locate_rows_from_birthday_tables(tables: BeautifulSoup) -> BeautifulSoup:
    rows = [table.select("tbody > tr") for table in tables]
    return rows[0] + rows[1]


def get_column_values(row: BeautifulSoup) -> list:
    return row.find_all("td")


def parse_column_values(column_values: list) -> dict:
    return {
        "groupName": column_values[1].text,
        "idolName": column_values[2].text,
        "birthYear": int(column_values[4].text),
        "birthMonth": int(column_values[5].text),
        "birthDay": int(column_values[6].text),
        "age": int(column_values[7].text),
        "gender": column_values[8].text
    }


def birthday_matches_day_and_month(birthday: dict) -> bool:
    """Check whether a given birthday matches today's date."""
    return (birthday["birthMonth"] == seoul_current_month and
            birthday["birthDay"] == seoul_current_day)


def get_todays_birthdays() -> list:
    birthdays = get_birthdays()

    return [birthday for birthday in birthdays if
            birthday_matches_day_and_month(birthday)]


def get_birthdays() -> list:
    """Retrieving data about upcoming idols' birthdays."""
    response = request_url(BIRTHDAY_URL)
    soup = convert_response_to_soup(response)
    tables = locate_birthday_tables(soup)
    rows = locate_rows_from_birthday_tables(tables)
    columns_values = [get_column_values(row) for row in rows]
    return [parse_column_values(
        columns_value) for columns_value in columns_values]


def generate_birthday_message(idol_name: str, idol_group: str) -> str:
    return f"Happy {idol_name} day ! \U0001F973\U0001F382\n\n" \
        f"{convert_expression_to_hashtag(idol_name)}" \
        f"{convert_expression_to_hashtag(idol_group)}" \
        f"{convert_expression_to_hashtag('Kpop')}" \
        f"{convert_expression_to_hashtag('Birthday')}"


if __name__ == "__main__":
    print(seoul_current_day, seoul_current_month)
    today = get_todays_birthdays()
    print(today)
    for ppl in today:
        print(generate_birthday_message(ppl))
        print("\n-------------------")
