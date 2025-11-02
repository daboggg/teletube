from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pytubefix import StreamQuery


def res_kb(streams:StreamQuery) -> InlineKeyboardMarkup:
    res: list = [s.resolution for s in streams if not s.is_progressive]

    ikb = InlineKeyboardBuilder()

    for r in res:
        ikb.button(text=r, callback_data=f'!@#resolution#@!:{r}')

    return ikb.adjust(3).as_markup()
