import logging

from BirthdayBot.birthday import (generate_birthday_message,
                                  get_todays_birthdays)
from BirthdayBot.google_images import download_idol_picture
from BirthdayBot.twitter_bot import TwitterBot

logging.basicConfig(level=logging.INFO)
bot = TwitterBot()


def main() -> None:
    if not bot.has_posted_today():
        birthdays = get_todays_birthdays()
        for birthday in birthdays:
            idol_name, idol_group = birthday["idolName"], birthday["groupName"]
            message = generate_birthday_message(idol_name, idol_group)
            picture_path = download_idol_picture(idol_name, idol_group)
            if picture_path is None:
                bot.tweet(message)
            else:
                bot.tweet_with_picture(message, picture_path)
    else:
        logging.info("Nothing posted because already posted today")


if __name__ == "__main__":
    main()
