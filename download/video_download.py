import asyncio
import os
from aiogram import types
from aiogram.types import FSInputFile
from pytubefix import YouTube
from pytubefix.cli import on_progress

from keyboard.bot_keyboard import keyboard


async def download_video(message: types.Message, video_url: str):
    """
    Скачиваем видео ролик ТОЛЬКО YOUTUBE.
    Тут шутки и приколы в сторону user, что бы скучно не было )
    """
    try:
        await message.answer('Серьёзно, ты ещё это и посмотреть хочешь')
        await asyncio.sleep(3)

        await message.bot.send_sticker(
            message.from_user.id,
            sticker="CAACAgIAAxkBAAEGUSxmdT0kAVXqpzyMcd9UarhSI4tpQAAC9gQAAhnydRtt4ksfOtJBXTUE")

        link_video = YouTube(video_url, on_progress_callback=on_progress)  # Тут вызывается функция для загрузки
        stream = link_video.streams.get_highest_resolution()

        if stream:

            video_path = f'Видео/{link_video.title}'
            stream.download(output_path='Видео/', filename=link_video.title)
            await message.answer('Почти готово')

            await asyncio.sleep(3)

            await message.answer("Вшиваю майнер👀")

            video_file_input = FSInputFile(video_path)

            chat_id = message.chat.id
            await message.bot.send_video(chat_id=chat_id, video=video_file_input, caption="Ваше видео.")

            os.remove(video_path)
            await message.answer('Видео успешно скачано и отправлено! Теперь иди от сюда :)', reply_markup=keyboard)
        else:
            await message.answer('Не удалось найти аудиопоток.')

    except Exception as e:
        await message.answer(f"Произошла ошибка при извлечении аудио: {e}")
