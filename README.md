# Korean Drama Bot

This project is a Telegram bot that helps users find and download Korean drama episodes. It utilizes web scraping to search for dramas and episodes on dramacool.bg.

## Setup
1. Install the required packages using `pip install -r requirements.txt`.
2. Create a `.env` file with your Telegram Bot API token as `BOT_TOKEN=your_bot_token`.

## Usage
1. Start the bot by running `python bot.py`.
2. Send the name of a K-drama movie to the bot.
3. Choose a drama from the list provided.
4. Select an episode to get the download link.

## Files
- `crawler.py`: Contains functions for searching dramas, getting drama episodes, and extracting download links.
- `bot.py`: Implements the Telegram bot functionality using the aiogram library.

Feel free to explore and enhance the functionality of this bot!
