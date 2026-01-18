import datetime
from aiogram import Bot
from settings import TOKEN, ADMIN, NAME_BOT


async def send_message_bot(chat_id, text, markup=None, message_id: int = None):
    async with Bot(token=TOKEN).context(True) as bot:
        if message_id:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup)
        else:
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode="HTML")


async def send_report_admin(flag: bool = True):
    time = datetime.datetime.now()
    if flag:
        text = f'Бот {NAME_BOT} работает.\n{time}'
    else:
        text = f'Падение бота {NAME_BOT}\n{time}'
    await send_message_bot(ADMIN, text)
