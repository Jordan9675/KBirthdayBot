import logging
import os
from datetime import datetime
from typing import Tuple

import pytz
import tweepy

from birthday_bot.birthday import seoul_current_day, seoul_current_month
from birthday_bot.utils import delete_file

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
SEOUL_TIMEZONE = pytz.timezone('Asia/Seoul')


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
        """Return date of last tweet (Seoul time)"""
        last_post = self.api.user_timeline(
            count=25, include_rts=False, exclude_replies=True)[0].created_at

        return pytz.utc.localize(last_post).astimezone(SEOUL_TIMEZONE)

    def has_posted_today(self) -> bool:
        """Check whether the bot has already posted today based on Seoul time"""
        current_date = datetime.now(SEOUL_TIMEZONE)
        last_post_date = self.get_last_post_created_date()

        return current_date.date() == last_post_date.date()

    def upload_media(self, media_path: str) -> int:
        """Upload media to Twitter and returns its Twitter ID"""

        return self.api.media_upload(filename=media_path).media_id

    def tweet_with_picture(self, message: str, picture_path: str) -> None:
        try:
            media_id = self.upload_media(media_path=picture_path)
            self.api.update_status(status=message, media_ids=[media_id])
        except tweepy.error.TweepError:
            self.tweet(message)
        finally:
            delete_file(picture_path)

    def tweet(self, message: str) -> None:
        self.api.update_status(message)
