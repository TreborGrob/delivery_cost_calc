import logging
from tg_bot.resources import FormatTextTags


async def reminder_info(requests_users: dict) -> str:
    answer_text = f"{FormatTextTags.STRONG_OPEN_TAG}Пользовались ботом:{FormatTextTags.STRONG_CLOSE_TAG}\n\n"
    for key, value in requests_users.items():
        value_data = value.split("_")
        nickname = "_".join(value_data[:-1])
        count_requests = value_data[-1]
        answer_text += f"Tg_id: {key} - Nickname: {nickname} - Запросов: {count_requests}\n"
    try:
        requests_users.clear()
        return answer_text
    except Exception as e:
        logging.info(e)
        return ""
