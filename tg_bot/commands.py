from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from settings import ADMIN
from tg_bot.resources import CommandsTitle
from tg_bot.utils.schedule_funcs import reminder_info

router = Router()


@router.message(Command(CommandsTitle.START.value))
async def start_bot(message: Message):
    await message.answer("Бот для расчёта стоимости доставки\nВведи город куда нужна доставка")


@router.message(Command(CommandsTitle.REPORT.value))
async def report_info(message: Message, requests_users: dict):
    if message.from_user.id == ADMIN:
        answer_text = await reminder_info(requests_users)
        await message.answer(answer_text)


@router.message(Command(CommandsTitle.REPORT_CLEAR.value))
async def report_clear(message: Message, requests_users: dict):
    if message.from_user.id == ADMIN:
        requests_users.clear()
        answer_text = "Dict requests_user clear."
        await message.answer(answer_text)
