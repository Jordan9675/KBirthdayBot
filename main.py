import logging

from birthday_bot.birthday import (generate_birthday_message,
                                   get_todays_birthdays)
from birthday_bot.google_images import (DOWNLOADER_OUTPUT_DIR,
                                        download_idol_picture)
from birthday_bot.twitter_bot import TwitterBot
from birthday_bot.utils import delete_folder

logging.basicConfig(level=logging.INFO)
bot = TwitterBot()


def main() -> None:
    if not bot.has_posted_today():
        birthdays = get_todays_birthdays()
        for birthday in birthdays:
            idol_name, idol_group = birthday["idolName"], birthday["groupName"]
            message = generate_birthday_message(idol_name, idol_group)
            picture_path = download_idol_picture(idol_name, idol_group)
            bot.tweet_with_picture(message, picture_path)
        delete_folder(DOWNLOADER_OUTPUT_DIR)
    else:
        logging.info("Nothing posted because already posted today")


if __name__ == "__main__":
    main()
