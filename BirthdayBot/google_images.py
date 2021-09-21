import logging
import os
import random

import requests

from .utils import download_file_from_url, remove_extra_space

API_KEYS = [
    os.getenv("SERPAPI_KEY_1"),
    os.getenv("SERPAPI_KEY_2"),
    os.getenv("SERPAPI_KEY_3")
]
URL = "https://serpapi.com/search?ijn=0&q={}&tbm=isch&hl=en&tbs=isz:m&api_key={}"
VALID_IMG_EXTENSIONS = [".jpg", ".png", ".jpeg"]


def url_has_extension(url: str, accepted_extensions: list) -> bool:
    """Check whether the file's path got one of the extensions"""
    return any(extension in url.lower() for extension in accepted_extensions)


def request_google_image(query: str) -> dict:
    """Make a request to the Google Image API"""
    for api_key in API_KEYS:
        url = URL.format(query, api_key)
        response = requests.get(url).json()
        if "error" in response:
            logging.info("Couldn't use API Key %s", api_key)
        else:
            return response


def get_urls_from_google_image_api_response(google_response: dict) -> list:
    results = google_response["images_results"]

    return [result["original"] for result in results]


def get_url_of_first_google_image_result(query: str) -> str:
    google_image_api_response = request_google_image(query)
    urls = get_urls_from_google_image_api_response(google_image_api_response)
    urls = [url for url in urls if url_has_extension(
        url, VALID_IMG_EXTENSIONS)]

    return urls[0]


def get_idol_picture(idol_name: str, idol_group: str) -> str:
    query = f"{idol_name} {idol_group} kpop"
    query = remove_extra_space(query)

    return get_url_of_first_google_image_result(query)


def add_extension_to_filename_given_url(filename: str, url: str) -> str:
    for extension in VALID_IMG_EXTENSIONS:
        if extension in url:
            return filename + extension


def download_idol_picture(idol_name: str, idol_group: str,
                            max_retries: int = 3) -> str:
    """Download random picture from an idol and returns its local path"""
    picture_url = get_idol_picture(idol_name, idol_group)
    filename = f"{idol_name}_{idol_group}"
    filename = add_extension_to_filename_given_url(filename, picture_url)

    for _ in range(max_retries):
        try:
            download_file_from_url(picture_url, filename)
            return filename
        except BaseException:
            logging.exception("Couldn't download picture from %s", picture_url)

    return None
