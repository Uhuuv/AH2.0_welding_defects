import asyncio
import logging
import sys
import model
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram import F

TOKEN = '7455470086:AAE4QbNm5Rh7IjvyK6LEOFQEd-TA97DNVt0'    # токен бота
lastMessage = ""

dp = Dispatcher()


# Хендлер на команду /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_data = message.from_user.full_name
    greeting_message = (f"Здравствуйте, {user_data}!")
    await message.answer(f'{greeting_message}')
    await message.answer( "Загрузите фотографию сварного шва, чтобы обнаружить дефекты."
                          " Фотографии будут обрабатываться по очереди."
                          " На обработку может уйти некоторое время.")
    await message.bot.unpin_all_chat_messages(message.chat.id)
    await message.bot.pin_chat_message(message.chat.id, message.message_id + 2, True)


# Хендлер на прием фотографии
@dp.message(F.photo)
async def picture_handler(message: Message, bot: Bot) -> None:
    current_picture_name = message.photo[-1].file_unique_id + '.jpg'
    global lastMessage
    await message.bot.download(file=message.photo[-1].file_id, destination = 'data/' + current_picture_name)

    waitMessage = "Идет обработка, ждите..."
    if lastMessage != waitMessage:
        lastMessage = waitMessage
        await bot.send_message(message.chat.id, waitMessage)

    input_image_path = 'data/' + current_picture_name
    model_path = 'AI_model/best.pt'
    output_images_path = 'outputs/images'

    answer_path = model.picture_handling(input_image_path, model_path, output_images_path)
    picture = FSInputFile(path=answer_path)
    await bot.send_photo(message.chat.id, photo=picture)
    os.remove('data/' + current_picture_name)
    lastMessage = "pic"


#Хендлер на прием фотографии файлом
@dp.message(F.document)
async def picture_file_handler(message: Message, bot: Bot) -> None:
    current_picture_name = message.document.file_unique_id + '.jpg'
    global lastMessage
    await message.bot.download(file=message.document.file_id, destination = 'data/' + current_picture_name)

    waitMessage = "Идет обработка, ждите..."
    if lastMessage != waitMessage:
        lastMessage = waitMessage
        await bot.send_message(message.chat.id, waitMessage)

    input_image_path = 'data/' + current_picture_name
    model_path = 'AI_model/best.pt'
    output_images_path = 'outputs/images'

    answer_path = model.picture_handling(input_image_path, model_path, output_images_path)
    picture = FSInputFile(path=answer_path)
    await bot.send_photo(message.chat.id, photo=picture)
    os.remove('data/' + current_picture_name)
    lastMessage = "pic"

# Хендлер на прием видео
@dp.message(F.video)
async def picture_handler(message: Message, bot: Bot) -> None:
    await bot.send_message(message.chat.id, "Извините, обработка видео не поддерживается")


# Хендлер на прием анимации
@dp.message(F.animation)
async def picture_handler(message: Message, bot: Bot) -> None:
    await bot.send_message(message.chat.id, "Извините, обработка анимаций не поддерживается")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())