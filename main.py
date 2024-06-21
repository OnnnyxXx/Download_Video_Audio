import asyncio
import os
import random
from aiogram import types, F
from aiogram.types import InputFile, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pytube import YouTube
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
import logging

token = '6136167557:AAHEohAi6jN0yQERVRuUp6AdaGKi3StxoYU'
bot = Bot(token)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание клавиатуры
builder = InlineKeyboardBuilder()
builder.add(InlineKeyboardButton(text="Скачать Аудио", callback_data="download_audio"))
builder.add(InlineKeyboardButton(text="Скачать Видео", callback_data="download_video"))
keyboard = builder.as_markup()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Стартовое меню с приветствием и кнопками.

    Нужно добавить GIF.....

    """
    gif_file_funny = FSInputFile("hello_user/kiss-lip-kiss.gif")
    # ....
    # builder = InlineKeyboardBuilder()
    # builder.add(types.InlineKeyboardButton(text="Скачать Аудио", callback_data="download_audio"))
    # builder.add(types.InlineKeyboardButton(text="Скачать Видео", callback_data="download_video"))
    # .....
    await message.answer(f'Привет, {message.from_user.first_name}!')
    await bot.send_animation(chat_id=message.chat.id, animation=gif_file_funny, reply_markup=keyboard)


user_data = {}  # Храним пользователей и type, audio or video


@dp.callback_query(lambda c: c.data == "download_audio")
async def get_link_audio(callback_query: types.CallbackQuery):
    """
    Проверяем что user нажал на download_audio в def cmd_start.
    """
    user_data[callback_query.from_user.id] = {'type': 'audio'}
    await callback_query.message.answer("Пожалуйста, отправьте ссылку на видео для скачивания аудио.")


@dp.callback_query(lambda c: c.data == "download_video")
async def get_link_video(callback_query: types.CallbackQuery):
    """
    Проверяем что user нажал на download_video в def cmd_start.
    Так-же присваиваем type в user_data
    """
    user_data[callback_query.from_user.id] = {'type': 'video'}
    await callback_query.message.answer("Пожалуйста, отправьте ссылку на видео для скачивания видео.")


@dp.message()
async def save_link_and_download(message: types.Message):
    """
    Передаем тип и ссылку в def на скачивания либо аудио либо видео.
    И наче просим выбрать что ему нужно скачать.
    """
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Пожалуйста, выберите, что вы хотите скачать, используя кнопки.")

    user_data[user_id]['url'] = message.text
    if user_data[user_id]['type'] == 'audio':
        await download_audio(message, user_data[user_id]['url'])
    elif user_data[user_id]['type'] == 'video':
        await download_video(message, user_data[user_id]['url'])


async def download_audio(message: types.Message, audio_url: str):
    """
    Скачиваем аудио с видео ролика ТОЛЬКО YOUTUBE.
    Тут шутки и приколы в сторону user, что бы скучно не было )
    """
    try:
        await message.answer('ВООУУУ, я посмотрел что там, поэтому я..')
        link_audio = YouTube(audio_url)
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

            await bot.send_audio(chat_id=chat_id, audio=audio_file_input, caption="Ваше аудио, приятного прослушивания")
            await bot.send_sticker(
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


# ///////////////////////////////////////////////////

async def download_video(message: types.Message, video_url: str):
    """
    Скачиваем видео ролик ТОЛЬКО YOUTUBE.
    Тут шутки и приколы в сторону user, что бы скучно не было )
    """
    try:
        await message.answer('Серьёзно, ты ещё это и посмотреть хочешь')
        await asyncio.sleep(3)

        await bot.send_sticker(
            message.from_user.id,
            sticker="CAACAgIAAxkBAAEGUSxmdT0kAVXqpzyMcd9UarhSI4tpQAAC9gQAAhnydRtt4ksfOtJBXTUE")

        link_video = YouTube(video_url)
        stream = link_video.streams.get_highest_resolution()

        if stream:

            video_path = f'Видео/{link_video.title}'
            stream.download(output_path='Видео/', filename=link_video.title)
            await message.answer('Почти готово')

            await asyncio.sleep(3)

            await message.answer("Вшиваю майнер👀")

            video_file_input = FSInputFile(video_path)

            chat_id = message.chat.id
            await bot.send_video(chat_id=chat_id, video=video_file_input, caption="Ваше видео.")

            os.remove(video_path)
            await message.answer('Видео успешно скачано и отправлено! Теперь иди от сюда :)', reply_markup=keyboard)
        else:
            await message.answer('Не удалось найти аудиопоток.')

    except Exception as e:
        await message.answer(f"Произошла ошибка при извлечении аудио: {e}")


async def main():
    """
    Передаем bot в dp -> Dispatcher() 14 строка.
    """
    await dp.start_polling(bot)


if __name__ == "__main__":
    """Запускаем main в асинхронном режиме )"""
    asyncio.run(main())
