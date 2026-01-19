import asyncio
import logging
import platform

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from settings import CDEK_LOGIN, CDEK_PASSWORD, TOKEN
from tg_bot import commands, handlers
from tg_bot.log_work import setup_logging
from tg_bot.send_message_bot import send_report_admin
from tg_bot.shipping.api_cdek import CDEKClient


async def main():
    # Настройка хранилища и логгирования
    storage = MemoryStorage()
    logging.basicConfig(level=logging.INFO)

    # Инициализация бота
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

    # Инициализация диспетчера
    dp = Dispatcher(storage=storage)

    # Подключаем роутеры
    dp.include_routers(commands.router, handlers.router)

    # Запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)

    # Сессия для запросов
    cdek_client = CDEKClient(client_id=CDEK_LOGIN, client_secret=CDEK_PASSWORD, is_test=False)

    dp["cdek_client"] = cdek_client

    try:
        await dp.start_polling(bot)
    finally:
        await cdek_client.close()
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        setup_logging()
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
    finally:
        asyncio.run(send_report_admin(False))

