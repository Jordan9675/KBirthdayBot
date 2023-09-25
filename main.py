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
    #if not bot.has_posted_today():
    birthdays = get_todays_birthdays()
    for birthday in birthdays:
        idol_name, idol_group = birthday["idolName"], birthday["groupName"]
        message = generate_birthday_message(idol_name, idol_group)
        try:
            # picture_path = download_idol_picture(idol_name, idol_group)
            #bot.tweet_with_picture(message, picture_path)
            bot.tweet(message)
        except Exception as exc:
            logging.error(exc)
            logging.info("Posting without picture.")
            bot.tweet(message)
    delete_folder(DOWNLOADER_OUTPUT_DIR)



if __name__ == "__main__":
    main()
