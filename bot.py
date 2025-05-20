import os
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv  # для загрузки токена из файла .env (при локальном запуске)

# Загрузка переменных окружения из .env, если файл существует
load_dotenv()

# Получение токена и chat_id из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPPORT_CHAT_ID = os.getenv("SUPPORT_CHAT_ID")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start — отправляет приветственное сообщение пользователю
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Здравствуйте! 🤖 Я бот поддержки. Напишите свой вопрос или опишите проблему, и я передам ваше сообщение специалистам.")

# Обработчик всех остальных текстовых сообщений от пользователя
@dp.message_handler(content_types=types.ContentType.TEXT)
async def forward_to_support(message: types.Message):
    username = message.from_user.username or message.from_user.full_name
    text = message.text
    # Формируем сообщение для группы: никнейм пользователя + текст обращения
    forward_text = f"@{username}: {text}"
    # Отправляем сообщение в группу техподдержки
    await bot.send_message(chat_id=SUPPORT_CHAT_ID, text=forward_text)
    # Отправляем пользователю подтверждение
    await message.answer("✅ Ваше обращение отправлено в поддержку. Мы скоро свяжемся с вами.")

# Запуск бота (долгий опрос Telegram на новые сообщения)
if __name__ == "__main__":
    executor.start_polling(dp)
