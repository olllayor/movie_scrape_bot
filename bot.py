from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup
from dotenv import load_dotenv
from crawler import search_dramas, drama_episodes, download_btn
import logging
import os

load_dotenv()


logging.basicConfig(level=logging.INFO)
# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# This dictionary maps short identifiers to URLs
url_map = {}



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome to the Korean Movie Bot!\n\n\nSend me the name of a K-drama movie, and I'll try to find it for you.\n\n\n‼️ Please enter the name of the movie as completely as possible")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    global url_map
    query = message.text
    dramas = search_dramas(query)

    if dramas:
        keyboard = InlineKeyboardMarkup()
        for idx, drama in enumerate(dramas):
            callback_data = f"drama_{idx}"
             # Now storing a dictionary with both URLs
            url_map[callback_data] = {"url": drama['url'], "image_url": drama['image_url'], "name": drama['name']}
            keyboard.add(types.InlineKeyboardButton(text=drama['name'], callback_data=callback_data))
        await message.answer("🎬 Choose a drama:", reply_markup=keyboard)
    else:
        await message.reply("Sorry, I couldn't find any matching movies.")


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('drama_'))
async def handle_drama_selection(callback_query: types.CallbackQuery):
    drama_details = url_map.get(callback_query.data)
    if not drama_details:
        await bot.send_message(callback_query.from_user.id, "Error: Drama details not found.")
        return
    
    # Sending the drama image to the user
    drama_name = drama_details.get("name", "Selected Drama")
    await bot.send_photo(callback_query.from_user.id, drama_details["image_url"], caption=drama_name)

    episodes = drama_episodes(drama_details["url"])
    keyboard = types.InlineKeyboardMarkup()
    for idx, episode in enumerate(episodes):
        callback_data = f"episode_{idx}"
        # Assuming episodes also have URLs and possibly image URLs; adjust as necessary
        url_map[callback_data] = episode['url']
        keyboard.add(types.InlineKeyboardButton(text=episode['name'], callback_data=callback_data))
    
    await bot.send_message(callback_query.from_user.id, "🎞 Select an episode:", reply_markup=keyboard)

# Handler for when an episode is selected
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('episode_'))
async def handle_episode_selection(callback_query: types.CallbackQuery):
    # Retrieve the episode URL from the url_map using the callback_data
    episode_url = url_map.get(callback_query.data)
    if not episode_url:
        await bot.send_message(callback_query.from_user.id, "Error: Episode URL not found.")
        return
    
    # Here you would call your function to get the download button page URL
    # For this example, let's say download_btn returns the direct URL or None
    download_page_url = download_btn(episode_url)  # This needs to be defined or imported
    
    if download_page_url:
        # Create a button that links directly to the download page
        keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Go to Download Page", url=download_page_url))
        await bot.send_message(callback_query.from_user.id, "Click the button below to download the episode:", reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, "Sorry, the download page could not be found.")
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
