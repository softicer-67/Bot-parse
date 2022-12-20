import asyncio
import json
# import logging
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink, hide_link
from config import token

# logging.basicConfig(level=logging.INFO)

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def on_startup(_):
    channel = '@all_new_all'
    with open("all_posts.json", 'r', encoding='utf-8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f"{v['post_title']}\n{hide_link(v['post_img'])}"
        await bot.send_message(channel, news)
    raise sys.exit()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


