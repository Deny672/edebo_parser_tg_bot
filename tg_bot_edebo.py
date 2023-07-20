import aiogram
from parser_edebo import main
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from gitignore import token

bot = Bot(token=token)
db = Dispatcher(bot)

@db.message_handler(commands='start')
async def start(message: types.Message):
    start_buttnos = ['Детальна інформація', 'Підтримати розробника']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttnos)
    await message.answer('Привіт, я бот створений для того, щоб тобі було зручніше дізнатись інформацію про тих хто вступає в твій виш на твою спеціальність', reply_markup=keyboard)

@db.message_handler(Text(equals='Детальна інформація'))
async def dop_info(message: types.Message):
    await message.answer('Щоб розпочати роботу, мені потрібен код, як його отримати можна побачити на фото, він виокремлений червоним кольором')
    with open('Приклад.png', 'rb') as file:
        await bot.send_document(message.chat.id, file)

    chat_id = message.chat.id


@db.message_handler(Text(equals='Підтримати розробника'))
async def info_razrab(message: types.Message):
    await message.answer('Я надішлю ссилку на свого розробника https://t.me/Deny_672')


@db.message_handler(content_types=types.ContentType.TEXT)
async def text_message(message: types.Message):
    chat_id = message.chat.id
    if not isinstance(message.text, str):
        return False

    if 7 <= len(message.text) <= 10:
        await message.answer('Процедура пошуку та зберігання інформації займе певний час, почекайте будь-ласка')

        file = await main(message.text)
        if file is not None:
            await bot.send_document(chat_id=chat_id, document=open(file, 'rb'))
        else:
            await message.answer('Ви ввели невірний код чи повідомлення')
        return True
    else:
        await message.answer('Ви ввели невірний код чи повідомлення')
        return False


if __name__ == '__main__':
    executor.start_polling(db)
