import aiohttp
from typing import Optional, Dict, Any
import msgspec
from tg_bot.shipping.models import CalculatorRequest, Location, Package


class CDEKClient:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            is_test: bool = True
    ):
        self.client_id = "wqGwiQx0gg8mLtiEKsUinjVSICCjtTEP" if is_test else client_id
        self.client_secret = "RmAmgvSgSl1yirlz9QupbzOJVqhCxcP5" if is_test else client_secret
        self.base_url = "https://api.edu.cdek.ru" if is_test else "https://api.cdek.ru"
        self._session: Optional[aiohttp.ClientSession] = None
        self._token: Optional[str] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Создает сессию, если она еще не создана."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _get_token(self):
        """Получает или обновляет токен доступа."""
        if self._token:
            return self._token

        url = f"{self.base_url}/v2/oauth/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        session = await self._get_session()
        async with session.post(url, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Error auth: {resp.status}, {text}")
            data = await resp.json()
            self._token = data.get("access_token")
            return self._token

    async def _request(self, method: str, path: str, data: dict | bytes | None = None, params: dict | None = None):
        """ Единый запрос """
        token = await self._get_token()
        session = await self._get_session()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}{path}"
        kwargs = {
            "params": params,
            "headers": headers
        }
        if data is not None:
            if isinstance(data, bytes):
                kwargs["data"] = data
            else:
                kwargs["json"] = data
        async with session.request(method, url, **kwargs) as resp:
            if resp.status == 401:
                self._token = None
                return await self._request(method, path, data, params)

            return await resp.json()

    async def calculate_delivery(self, calc_data: CalculatorRequest) -> Dict[str, Any]:
        """ Расчет стоимости по конкретному тарифу. """
        payload = msgspec.json.encode(calc_data)

        return await self._request(
            method="POST",
            path="/v2/calculator/tariff",
            data=payload
        )

    async def location_by_name_city(self, city_name: str):
        """ Получаем локации по наименованию населённого пункта. """
        params = {
            "name": city_name
        }
        return await self._request(
            method="GET",
            path="/v2/location/suggest/cities",
            params=params
        )

    async def close(self):
        """Закрытие сессии."""
        if self._session:
            await self._session.close()
