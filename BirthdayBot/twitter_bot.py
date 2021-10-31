import logging
import os
from typing import Tuple

import tweepy

from .birthday import seoul_current_day, seoul_current_month
from .utils import delete_file
from datetime import datetime, timedelta

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")


class TwitterBot:

    def __init__(self) -> None:
        self.authenticate()

    def authenticate(self) -> None:
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)
        logging.info("Successfully authenticated")

    def get_last_post_created_date(self) -> Tuple[int, int]:
        """Return day and month of last tweet"""
        last_post = self.api.user_timeline(
            count=25, include_rts=False, exclude_replies=True)[0]

        return last_post.created_at.month, last_post.created_at.day

    def has_posted_today(self) -> bool:
        """Check whether the bot has already posted today"""
        current_date = datetime.now()
        last_post_month, last_post_day = self.get_last_post_created_date()

        return (current_date.month == last_post_month and
                current_date.day == last_post_day and
                (current_date + timedelta(days=1)).day == seoul_current_day and
                (current_date + timedelta(days=1)).month == seoul_current_month)

    def upload_media(self, media_path: str) -> int:
        """Upload media to Twitter and returns its Twitter ID"""

        return self.api.media_upload(filename=media_path).media_id

    def tweet_with_picture(self, message: str, picture_path: str) -> None:
        media_id = self.upload_media(media_path=picture_path)
        self.api.update_status(status=message, media_ids=[media_id])
        delete_file(picture_path)

    def tweet(self, message: str) -> None:
        self.api.update_status(message)
