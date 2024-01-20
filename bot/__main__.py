import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from aiogram.utils.exceptions import RetryAfter
from loguru import logger

from bot.config import settings
from bot.db import Manager
from bot.parser import get_data
from bot.parser import WebUrls
from bot.utilts import DataManager

BOT = Bot(settings.BOT_TOKEN)


async def send_media_to_channel(media: types.MediaGroup):
    """Send media to channel
    :param media: media to send
    :param time: time to sleep if RetryAfter exception
    """
    try:
        await BOT.send_media_group(settings.CHANNEL_ID, media=media)
    except RetryAfter as e:
        await asyncio.sleep(e.timeout)
        await send_media_to_channel(media=media, time=e.timeout)


async def scheduler():
    """Scheduler for sending data to channel"""
    database = Manager()
    web_parser = WebUrls()

    while True:
        logger.info("start sending data to channel")
        urls = web_parser.get_urls()

        data = await get_data(urls)
        db_data = database.select_data()

        data_manager = DataManager(db_data)

        for item in data:
            data_manager.check_data(item)

        data_manager.consume_data_to_db(database)

        for info in data_manager.new_data:
            await send_media_to_channel(
                media=data_manager.get_media(
                    info,
                    caption=f"<a href='{info[0]}'>{info[1]}</a>\n{info[2]}\n{info[3]}\n{info[4]}",
                )
            )

        for info in data_manager.change_data:
            await send_media_to_channel(
                media=data_manager.get_media(
                    info,
                    caption=f"<a href='{info[0]}'>{info[1]}</a>\nPRICE CHANGED: {info[2]}\n{info[3]}\n{info[4]}",
                )
            )

        for info in data_manager.delete_data:
            await send_media_to_channel(
                media=data_manager.get_media(
                    info,
                    caption=f"<a href='{info[0]}'>{info[1]}</a>\n{info[2]}\n{info[3]}\n{info[4]}\n SALED",
                )
            )

        logger.success("data sent to channel")
        await asyncio.sleep(settings.TIME)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    dp = Dispatcher(BOT)
    logger.success("script started")
    executor.start_polling(dp, loop=loop)
