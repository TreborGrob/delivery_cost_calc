import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv("TOKEN")
ADMIN = int(os.getenv("ADMIN"))

CDEK_LOGIN = os.getenv("CDEK_LOGIN")
CDEK_PASSWORD = os.getenv("CDEK_PASSWORD")

NAME_BOT = "amount_shipping"
ADD_FOR_SUMM = 150
CITY_DEFAULT = "Казань"
CITY_DEFAULT_CODE = 424
TARIFF_DEFAULT = 136  # склад-склад
