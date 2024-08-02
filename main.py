import asyncio
from aiogram import types
from aiogram.types import FSInputFile
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart

from config import TOKEN
import logging

from handlers.bot_handlers import router as hes_router

from keyboard.bot_keyboard import keyboard

token = TOKEN
bot = Bot(token)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Стартовое меню с приветствием и кнопками.

    Нужно добавить GIF.....

    """
    gif_file_funny = FSInputFile("other/hello_user/kiss-lip-kiss.gif")
    # ....
    # builder = InlineKeyboardBuilder()
    # builder.add(types.InlineKeyboardButton(text="Скачать Аудио", callback_data="download_audio"))
    # builder.add(types.InlineKeyboardButton(text="Скачать Видео", callback_data="download_video"))
    # .....
    await message.answer(f'Привет, {message.from_user.first_name}!')
    await bot.send_animation(chat_id=message.chat.id, animation=gif_file_funny, reply_markup=keyboard)


async def main():
    """
    Передаем bot в dp -> Dispatcher() 14 строка.
    """
    dp.include_router(hes_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    """Запускаем main в асинхронном режиме )"""
    asyncio.run(main())
