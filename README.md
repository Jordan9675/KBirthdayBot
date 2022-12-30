# KBirthdayBot

This repository holds all the source code used to power the [@KBirthdayBot](https://twitter.com/KBirthdayBot) Twitter account.

Each day, at **3PM UTC** (corresponding to Midnight Seoul Time), the bot will publish a Tweet to celebrate the birthday of the concerned idols.

The bot is posting via GitHub Actions while the data are retrieved from [dbkpop](https://dbkpop.com/).

Pictures posted along the Tweets are retrieved through using [google-images-download](https://github.com/hardikvasa/google-images-download). Please note that the repo has been copied into this current repo to fix some problems that remains on the original repo.

## Using the bot 

### Required registrations

To use this bot, it is necessary to register a Twitter App through the [Twitter Developer Platform](https://developer.twitter.com/en) so that you can interact with your Twitter account through the Twitter API.

### Setup

Create a python virtual environment with `python -m venv .venv` and then install the requirements with `pip install -r requirements.txt`

#### Environmental variables

This project use environmental variables to store the tokens from the Twitter App


Here are the fields to fill :

| Key                 	| Description                                                	|
|---------------------	|------------------------------------------------------------	|
| CONSUMER_KEY                	| Twitter App Consumer Key                                          	|
| CONSUMER_SECRET            	| Twitter App Consumer Secret                                      	|
| ACCESS_TOKEN 	| Twitter App Access Token                 	|
| ACCESS_TOKEN_SECRET         	| Twitter App Access Token Secret                                        	|

### Run

To run the bot, simply use the command `python main.py`.

Note that the bot will not post anything if it has already been runned the current day which allows to avoid your bot spamming.

## Troubleshooting

Please note that the bot may post Tweet to celebrate an idol's birthday without joining a picture to the Tweet. This is a known problem that is due to some troubles when updating the picture to Twitter. This will likely be solved in future updates.