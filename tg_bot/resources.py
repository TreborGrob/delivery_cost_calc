import enum


class CommandsTitle(enum.Enum):
    START = "start"


class FormatTextTags:
    # TICK = "✅"
    # CROSS = "❌"
    CODE_OPEN_TAG = "<code>"
    CODE_CLOSE_TAG = "</code>"
    STRONG_OPEN_TAG = "<strong>"
    STRONG_CLOSE_TAG = "</strong>"


class ClothName(enum.Enum):
    T_SHIRT = "Футболка"
    HOODIE = "Толстовка"
    FIRE_BOX_T_SHIRT = "Огненная коробка с футболкой"


TariffIdName = {136: "Посылка склад-склад",
                137: "Посылка склад-дверь"}
