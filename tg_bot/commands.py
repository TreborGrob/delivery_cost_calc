from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tg_bot.resources import CommandsTitle

router = Router()


@router.message(Command(CommandsTitle.START.value))
async def start_bot(message: Message):
    await message.answer("Бот для расчёта стоимости доставки\nВведи город куда нужна доставка")
