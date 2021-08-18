from BirthdayBot.birthday import get_todays_birthdays, generate_birthday_message
from BirthdayBot.twitter_bot import TwitterBot

bot = TwitterBot()

if __name__ == "__main__" and not bot.has_posted_today:
    birthdays = get_todays_birthdays()
    for birthday in birthdays:
        message = generate_birthday_message(birthday)
        bot.tweet(message)
