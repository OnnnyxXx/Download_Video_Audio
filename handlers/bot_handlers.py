from aiogram import types
from aiogram import Router

from download.audio_download import download_audio
from download.video_download import download_video

router = Router()

user_data = {}  # Храним пользователей и type, audio or video


@router.callback_query(lambda c: c.data == "download_audio")
async def get_link_audio(callback_query: types.CallbackQuery):
    """
    Проверяем что user нажал на download_audio в def cmd_start.
    """
    user_data[callback_query.from_user.id] = {'type': 'audio'}
    await callback_query.message.answer("Пожалуйста, отправьте ссылку на видео для скачивания аудио.")


@router.callback_query(lambda c: c.data == "download_video")
async def get_link_video(callback_query: types.CallbackQuery):
    """
    Проверяем что user нажал на download_video в def cmd_start.
    Так-же присваиваем type в user_data
    """
    user_data[callback_query.from_user.id] = {'type': 'video'}
    await callback_query.message.answer("Пожалуйста, отправьте ссылку на видео для скачивания видео.")


@router.message()
async def save_link_and_download(message: types.Message):
    """
    Передаем тип и ссылку в def на скачивания либо аудио, либо видео.
    Иначе просим выбрать что ему нужно скачать.
    """
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Пожалуйста, выберите, что вы хотите скачать, используя кнопки.")

    user_data[user_id]['url'] = message.text
    if user_data[user_id]['type'] == 'audio':
        await download_audio(message, user_data[user_id]['url'])
    elif user_data[user_id]['type'] == 'video':
        await download_video(message, user_data[user_id]['url'])
