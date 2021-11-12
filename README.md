# KBirthdayBot

This repository holds all the source code used to power the [@KBirthdayBot](https://twitter.com/KBirthdayBot) Twitter account.

Each day, at **3PM UTC** (corresponding to Midnight Seoul Time), the bot will publish a Tweet to celebrate the birthday of the concerned idols.

The bot is hosted on **Heroku** and the job is done through the **Heroku Scheduler** while the data are retrieved from [dbkpop](https://dbkpop.com/).

Pictures posted along the Tweets are retrieved through a Google Search using [SerpApi](https://serpapi.com/).

## Using the bot 

### Required registrations

To use this bot, it is necessary to :
- Register a Twitter App through the [Twitter Developer Platform](https://developer.twitter.com/en) so that you can interact with your Twitter account through the Twitter API.
- Register to [SerpApi](https://serpapi.com/) to dynamically retrieve pictures of idol's using the Google Search Engine.

### Setup

Create a python virtual environment with `python -m venv .venv` and then install the requirements with `pip install -r requirements.txt`

#### Environmental variables

This project use environmental variables to store the tokens from the Twitter App and the keys for the SerpApi API.

To set those environmental variables, fill the fields within the `.dummyenv` file and then rename it to `.env`.

Here are the fields to fill :

| Key                 	| Description                                                	|
|---------------------	|------------------------------------------------------------	|
| CONSUMER_KEY                	| Twitter App Consumer Key                                          	|
| CONSUMER_SECRET            	| Twitter App Consumer Secret                                      	|
| ACCESS_TOKEN 	| Twitter App Access Token                 	|
| ACCESS_TOKEN_SECRET         	| Twitter App Access Token Secret                                        	|
| SERPAPI_KEY_1      	| SerpAPI Key                                	|

*Note:* The name of the key(s) associated with the SerpAPI keys could be named according to your wishes as long as you ensure that you've specified the right environmental variables name within `birthday_bot/google_images.py`

*Note 2:* You can add as many SerpAPI keys as necessary as long as you also add them in `birthday_bot/google_images.py`. For the sake of this project, we registered to 5 API keys to ensure the good functionning of the bot along the month as one API key from a SerpApi free plan gives you access to a maximum of **100 requests** per month.

### Run

To run the bot, simply use the command `python main.py`.

Note that the bot will not post anything if it has already been runned the current day which allows to avoid your bot spamming.

## Troubleshooting

Please note that the bot may post Tweet to celebrate an idol's birthday without joining a picture to the Tweet. This is a known problem that is due to some troubles when updating the picture to Twitter. This will likely be solved in future releases.