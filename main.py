import asyncio
import os

from aiogram.dispatcher.filters import Text
import aiogram
import executor
from aiogram import Bot, Dispatcher, types
from pytube import YouTube

token = '6136167557:AAHEohAi6jN0yQERVRuUp6AdaGKi3StxoYU'
bot = Bot(token)
dp = Dispatcher(bot)

"""
Кнопку и функционал для скачки только аудио

"""


@dp.message_handler(commands=['start'])
async def start_commands(message: types.Message):
    start_button = ["Скачать видео и аудио"]  # "Скачать видео", 'Скачать Аудио'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await message.answer('Привет! {0.first_name} 👋'.format(message.from_user), reply_markup=keyboard)


@dp.message_handler(Text(equals='Скачать видео и аудио'))
async def get_link_audio(message: types.Message):
    await message.answer('Нужна ссылка на видос.....')


# @dp.message_handler(Text(equals='Скачать видео'))
# async def get_link_video(message: types.Message):
#     await message.answer("Пожалуйста, отправьте ссылку на видео для скачивания.")


@dp.message_handler()
async def download_audio(message: types.Message):
    """Загрузка Аудио"""
    try:
        link_audio = YouTube(message.text)
        stream = link_audio.streams.filter(only_audio=True).first()
        audio_path = f'Аудио/{link_audio.title}'
        stream.download(output_path='Аудио/', filename=link_audio.title)
        with open(audio_path, 'rb') as audio:
            await bot.send_audio(message.chat.id, audio, caption=f'Аудио от видео: {link_audio.title}')
        await message.answer('Аудио успешно извлечено и отправлено!')
        os.remove(audio_path)
    except Exception as e:
        await message.answer("Произошла ошибка при извлечении аудио")

    """Загрузка Видео"""
    try:
        link_video = YouTube(message.text)
        video_path = f'Видео/{link_video.title}'
        stream = link_video.streams.get_highest_resolution()
        stream.download(output_path='Видео/', filename=link_video.title)
        with open(video_path, 'rb') as video:
            await bot.send_video(message.chat.id, video, caption=link_video.title)
        await message.answer(f"Видео успешно скачано!")
        os.remove(video_path)
    except Exception as e:
        await message.answer("Произошла ошибка при загрузке видео")


async def main():
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
