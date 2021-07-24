from BirthdayBot.birthday import Birthday
from BirthdayBot.twitter_bot import TwitterBot

bot = TwitterBot()

if __name__ == "__main__":
    birthdays = Birthday.get_todays_birthdays()
    for birthday in birthdays:
        message = Birthday.generate_birthday_message(birthday)
        bot.tweet(message)
