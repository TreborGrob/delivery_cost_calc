from typing import List

import msgspec
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from settings import ADD_FOR_SUMM
from tg_bot.markups_keyboards import cart_items_markup, cities_markup
from tg_bot.resources import Buttons, ClothName
from tg_bot.shipping.api_cdek import CDEKClient
from tg_bot.shipping.models import CalculatorRequest, Location, Package, City
from tg_bot.units.units import Cloth

router = Router()


@router.message(F.text)
async def get_city(message: Message, state: FSMContext, cdek_client: CDEKClient):
    city_name = message.text
    raw_data = await cdek_client.location_by_name_city(city_name)
    try:
        cities = msgspec.convert(raw_data, List[City])
    except msgspec.ValidationError:
        await message.answer("Ошибка обработки данных от СДЭК")
        return

    if not cities:
        await message.answer("Город не найден")
        return

    if len(cities) > 1:
        await message.answer("Уточни город", reply_markup=await cities_markup(cities))
    else:
        await message.answer("Выбери посылку", reply_markup=await cart_items_markup())
        await state.update_data(city_code=cities[0].code)


@router.callback_query(F.data.startswith("city_"))
async def specify_city(callback: CallbackQuery, state: FSMContext, cdek_client: CDEKClient):
    city_code = callback.data.replace("city_", "")
    await state.update_data(city_code=city_code)
    await callback.message.edit_text("Выбери посылку", reply_markup=await cart_items_markup())


@router.callback_query(F.data.startswith("item_"))
async def calculation_shipping(callback: CallbackQuery, state: FSMContext, cdek_client: CDEKClient):
    item = callback.data.replace("item_", "")
    data = await state.get_data()
    city_code = int(data.get("city_code"))
    T_SHIRT = Cloth(ClothName.T_SHIRT.value, 200, 30, 30, 2)
    HOODIE = Cloth(ClothName.HOODIE.value, 800, 40, 35, 6)
    FIRE_BOX = Cloth(ClothName.FIRE_BOX_T_SHIRT.value, 500, 11, 20, 30)
    match item:
        case "HOODIE":
            unit = HOODIE
        case "T_SHIRT":
            unit = T_SHIRT
        case _:
            unit = FIRE_BOX
    calc = CalculatorRequest(
        type=1,
        from_location=Location(code=424, city="Казань"),  # Казань
        to_location=Location(code=city_code),  # код города получателя
        packages=[Package(weight=unit.weight, length=unit.length, width=unit.width, height=unit.height)],
        tariff_code=136  # Посылка склад-склад
    )
    text_answer = ""
    result = await cdek_client.calculate_delivery(calc)
    if "delivery_sum" in result:
        total_sum = int(result['delivery_sum'])+ADD_FOR_SUMM
        text_answer += (f"Стоимость: {Buttons.CODE_OPEN_TAG}{total_sum} руб.{Buttons.CODE_CLOSE_TAG}\n"
                        f"Срок: {Buttons.CODE_OPEN_TAG}{result['period_min']}-{result['period_max']} дн."
                        f"{Buttons.CODE_CLOSE_TAG}")
    else:
        if "errors" in result:
            error_message = result["errors"][0].get("message")
            text_answer += f"Ошибка: {error_message}"
    await callback.message.edit_text(text_answer)
    await state.clear()
