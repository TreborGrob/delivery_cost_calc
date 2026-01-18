import enum


class CommandsTitle(enum.Enum):
    START = "start"


class Buttons:
    TICK = "✅"
    CROSS = "❌"
    CODE_OPEN_TAG = "<code>"
    CODE_CLOSE_TAG = "</code>"


class ClothName(enum.Enum):
    T_SHIRT = "Футболка"
    HOODIE = "Толстовка"
    FIRE_BOX_T_SHIRT = "Огненная коробка с футболкой"
