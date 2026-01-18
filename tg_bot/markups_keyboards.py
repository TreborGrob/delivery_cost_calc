from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.resources import ClothName
from tg_bot.shipping.models import City


async def cart_items_markup() -> InlineKeyboardMarkup:
    """Клавиатура предметов"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text=ClothName.T_SHIRT.value, callback_data=f'item_{ClothName.T_SHIRT.name}'),
        InlineKeyboardButton(text=ClothName.HOODIE.value, callback_data=f'item_{ClothName.HOODIE.name}')
    )
    builder.row(InlineKeyboardButton(text=ClothName.FIRE_BOX_T_SHIRT.value,
                                     callback_data=f'item_{ClothName.FIRE_BOX_T_SHIRT.name}'))

    return builder.as_markup()


async def cities_markup(cities: list[City]) -> InlineKeyboardMarkup:
    """Клавиатура городов"""
    builder = InlineKeyboardBuilder()
    for city in cities:
        builder.row(
            InlineKeyboardButton(text=city.full_name, callback_data=f'city_{city.code}')
        )

    return builder.as_markup()

# if __name__ == "__main__":
#     print(ClothName.HOODIE.value)
