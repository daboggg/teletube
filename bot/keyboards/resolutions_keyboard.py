from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pytubefix import StreamQuery


def res_kb(streams:StreamQuery) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    for stream in streams:
        if stream.is_progressive:
            ikb.button(text=f'{stream.resolution}+', callback_data=f'!@#resolution#@!:{stream.resolution}')
        else:
            ikb.button(text=stream.resolution, callback_data=f'!@#resolution#@!:{stream.resolution}')

    return ikb.adjust(3).as_markup()
