import asyncio
import os
from aiogram import types
from aiogram.types import FSInputFile
from pytubefix import YouTube
from pytube.cli import on_progress

from keyboard.bot_keyboard import keyboard


async def download_audio(message: types.Message, audio_url: str):
    """
    Скачиваем аудио с видео ролика ТОЛЬКО YOUTUBE.
    Тут шутки и приколы в сторону user, что бы скучно не было )
    """
    try:
        await message.answer('ВООУУУ, я посмотрел что там, поэтому я..')
        link_audio = YouTube(audio_url, on_progress_callback=on_progress)  # Тут вызывается функция для загрузки
        stream = link_audio.streams.filter(only_audio=True).first()
        if stream:
            await message.answer('Вызываю полицию на ваш адрес! 🚔🚨')
            audio_filename = f"{link_audio.title}.mp3"
            audio_path = f"Аудио/{audio_filename}"
            await asyncio.sleep(3)

            await message.answer('Ладно, Шутка ), кста ↓ ')
            stream.download(output_path='Аудио/', filename=audio_filename)

            await message.answer('Почти готово')

            await asyncio.sleep(3)

            await message.answer("Вшиваю майнер👀")

            audio_file_input = FSInputFile(audio_path)

            chat_id = message.chat.id

            await message.bot.send_audio(chat_id=chat_id, audio=audio_file_input, caption="Ваше аудио, приятного"
                                                                                          "прослушивания")
            await message.bot.send_sticker(
                message.from_user.id,
                sticker="CAACAgEAAxkBAAEGUTxmdT8I9Yg45FEFesy3wRfQOfu1cAACYwADwKwII3myhHDslxHDNQQ")

            os.remove(audio_path)

            await message.answer(
                'Аудио успешно извлечено и отправлено! Может хотите скачать видео?',
                reply_markup=keyboard)
        else:
            await message.answer('Не удалось найти аудиопоток.')
    except Exception as e:
        await message.answer(f"Произошла ошибка при извлечении аудио: {e}")


