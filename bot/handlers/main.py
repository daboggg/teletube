import asyncio
import logging
import os
import re
import shutil
import threading

import ffmpeg
from aiogram import Router, F, Bot
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile
from pytubefix import StreamQuery, Stream, YouTube

from bot.keyboards.resolutions_keyboard import res_kb
logger = logging.getLogger(__name__)

main_router = Router()


class YoutubeURLFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        pattern = r'^https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
        return re.match(pattern, message.text) is not None


class MainSG(StatesGroup):
    get_resolution = State()


@main_router.message(YoutubeURLFilter())
async def list_reminders(message: Message, state: FSMContext) -> None:
    await state.clear()

    yt = YouTube(message.text)
    all_streams: StreamQuery = yt.streams
    video_streams_mp4: StreamQuery = all_streams.filter(mime_type='video/mp4')

    await state.update_data(all_streams=all_streams)
    await state.update_data(title=yt.title)

    await message.answer('выберите разрешение', reply_markup=res_kb(video_streams_mp4))
    await state.set_state(MainSG.get_resolution)


@main_router.callback_query(MainSG.get_resolution, F.data.startswith("!@#resolution#@!"))
async def delay_remind(callback: CallbackQuery,bot: Bot, state: FSMContext) -> None:
    await callback.answer('Ожидайте загрузки...')
    tmp = callback.data.split(":")
    resolution = tmp[1]
    state_data = await state.get_data()
    all_streams: StreamQuery = state_data.get('all_streams')
    title: StreamQuery = state_data.get('title')

    video_stream: Stream = all_streams.filter(mime_type='video/mp4').filter(resolution=resolution).order_by(
        'is_progressive').last()

    try:
        if video_stream.is_progressive:
            await callback.message.answer_video(video_stream.url, caption=f'{title}')
        else:

            thread = threading.Thread(target=download_video, args=(video_stream, all_streams, title))
            thread.start()
            while thread.is_alive():
                await asyncio.sleep(20)
                await callback.message.answer('Идет загрузка...')

            await callback.message.answer_video(FSInputFile(f"tmp/{title}.mp4"), caption=f'{title}')

    except Exception as er:
        await callback.message.answer('Что-то пошло не так... Попробуйте еще раз!')
        logger.error(er)
    finally:
        if os.path.exists('tmp'):
            shutil.rmtree('tmp')
        await state.clear()


@main_router.message()
async def error(message: Message):
    await message.answer('введите Youtube url')


def download_video(video_stream, all_streams, title):
    video_stream.download('tmp', filename='video.mp4')
    audio_stream = all_streams.filter(mime_type='audio/mp4').order_by('abr').last()
    audio_stream.download('tmp', filename='audio.mp4')

    input_video = ffmpeg.input('tmp/video.mp4')
    input_audio = ffmpeg.input('tmp/audio.mp4')
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'tmp/{title}.mp4').run()
