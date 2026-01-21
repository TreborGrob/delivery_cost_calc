import logging
from typing import List

import msgspec
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from settings import ADD_FOR_SUMM, CITY_DEFAULT, CITY_DEFAULT_CODE, TARIFF_DEFAULT, TARIFF_WAREHOUSE_DOOR
from tg_bot.markups_keyboards import cart_items_markup, cities_markup
from tg_bot.resources import FormatTextTags, ClothName, TariffIdName
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
        from_location=Location(code=CITY_DEFAULT_CODE, city=CITY_DEFAULT),
        to_location=Location(code=city_code),  # код города получателя
        packages=[Package(weight=unit.weight, length=unit.length, width=unit.width, height=unit.height)],
        tariff_code=TARIFF_DEFAULT
    )

    try:
        result = await cdek_client.calculate_delivery(calc)

        # Если тариф не подошел, пробуем второй тариф
        if "errors" in result:
            calc.tariff_code = TARIFF_WAREHOUSE_DOOR
            result = await cdek_client.calculate_delivery(calc)

    except Exception as e:
        # Если API СДЭК выдало 502/503 или вообще недоступно
        await callback.message.edit_text("Сервис СДЭК временно недоступен. Попробуйте позже.")
        logging.info(e)
        await state.clear()
        return  # Выходим из функции

    # Теперь проверяем результат (после всех попыток)
    if "delivery_sum" in result:
        tariff_name = TariffIdName.get(calc.tariff_code, "Стандартный")
        total_sum = int(result['delivery_sum']) + ADD_FOR_SUMM
        text_answer = (
            f"Тариф: <b>{tariff_name}</b>\n"
            f"Стоимость: <code>{total_sum} руб.</code>\n"
            f"Срок: <code>{result['period_min']}-{result['period_max']} дн.</code>"
        )
    elif "errors" in result:
        # Если СДЭК ответил, но сообщил об ошибке (например, город не найден)
        error_message = result["errors"][0].get("message", "Неизвестная ошибка")
        text_answer = f"Ошибка СДЭК: {error_message}"
    else:
        # На случай странных ответов
        text_answer = "Не удалось рассчитать стоимость. Проверьте данные."

    await callback.message.edit_text(text_answer)
    await state.clear()
