import logging
import os
from datetime import datetime
from typing import Tuple

import pytz
import tweepy

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
SEOUL_TIMEZONE = pytz.timezone("Asia/Seoul")


class TwitterBot:
    def __init__(self) -> None:
        self.authenticate()

    def authenticate(self) -> None:
        self.client = tweepy.Client(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        logging.info("Successfully authenticated")

    def get_last_post_created_date(self) -> Tuple[int, int]:
        """Return date of last tweet (Seoul time)"""
        last_post = self.client.user_timeline(
            count=25, include_rts=False, exclude_replies=True
        )[0].created_at

        return pytz.utc.localize(last_post).astimezone(SEOUL_TIMEZONE)

    def has_posted_today(self) -> bool:
        """Check whether the bot has already posted today based on Seoul time"""
        current_date = datetime.now(SEOUL_TIMEZONE)
        last_post_date = self.get_last_post_created_date()

        return current_date.date() == last_post_date.date()

    def upload_media(self, media_path: str) -> int:
        """Upload media to Twitter and returns its Twitter ID"""

        return self.client.media_upload(filename=media_path).media_id

    def tweet_with_picture(self, message: str, picture_path: str) -> None:
        try:
            media_id = self.upload_media(media_path=picture_path)
            self.client.update_status(status=message, media_ids=[media_id])
        except tweepy.error.TweepError:
            self.tweet(message)

    def tweet(self, message: str) -> None:
        self.client.create_tweet(message)
