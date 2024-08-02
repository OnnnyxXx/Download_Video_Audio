from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Создание клавиатуры
builder = InlineKeyboardBuilder()
builder.add(InlineKeyboardButton(text="Скачать Аудио", callback_data="download_audio"))
builder.add(InlineKeyboardButton(text="Скачать Видео", callback_data="download_video"))
keyboard = builder.as_markup()