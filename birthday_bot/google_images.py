import os
import random

from birthday_bot.google_images_download import google_images_download

DOWNLOADER_OUTPUT_DIR = "./downloads"

downloader = google_images_download.googleimagesdownload()


def download_image(google_query: str, filetype: str, limit: int, size: str) -> None:
    """Download images from Google Images"""
    query = {
        "keywords": google_query,
        "format": filetype,
        "limit": limit,
        "size": size,
    }
    downloader.download(query)


def select_picture_from_folder(folder: str, random_choice: bool) -> str:
    """Select a picture from a folder, either the first one or a random one
    if random_choice = True is passed"""
    pictures = os.listdir(folder)
    if random_choice:
        picture = random.choice(pictures)
    picture = pictures[0]
    return f"{folder}/{picture}"


def download_idol_picture(
    idol_name: str, idol_group: str, random_choice: bool = False
) -> str:
    """Download an idol's pictures and return the path to the downloaded items."""
    query = f"{idol_name} {idol_group} kpop"
    download_image(google_query=query, filetype="jpg", limit=5, size="medium")
    return select_picture_from_folder(f"{DOWNLOADER_OUTPUT_DIR}/{query}", random_choice)
