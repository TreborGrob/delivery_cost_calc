import msgspec
from typing import List, Optional


# Настройка: omit_defaults=True не будет включать пустые поля в JSON при отправке в СДЭК
class BaseStruct(msgspec.Struct, omit_defaults=True):
    pass


class City(BaseStruct):
    city_uuid: str
    code: int
    full_name: str
    country_code: str


class Location(BaseStruct):
    # Указываем значения по умолчанию прямо в полях
    code: Optional[int] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    contragent_type: str = "INDIVIDUAL"
    longitude: Optional[float] = None
    latitude: Optional[float] = None


class Package(BaseStruct):
    weight: int
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


class CalculatorRequest(BaseStruct):
    type: int
    from_location: Location
    to_location: Location
    packages: List[Package]
    tariff_code: Optional[int] = None
