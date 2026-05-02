import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

TOKEN = 8228321718:AAFSpJiy0rcXNdH-lZ4RVwSlFDCGw_BgSaY
GROUP_ID = -1001234567890

bot = Bot(token=TOKEN)
dp = Dispatcher()

# хранение объявлений
ads = {}

# ---------------- START ----------------
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Отправь /anketa чтобы создать объявление")

# ---------------- АНКЕТА ----------------
@dp.message(Command("anketa"))
async def anketa(message: types.Message):
    ads[message.from_user.id] = {}
    await message.answer("📍 Введи город:")

@dp.message()
async def form(message: types.Message):
    uid = message.from_user.id

    if uid not in ads:
        return

    data = ads[uid]

    # 1 шаг — город
    if "city" not in data:
        data["city"] = message.text
        await message.answer("📝 Теперь напиши текст объявления:")
        return

    # 2 шаг — текст
    if "text" not in data:
        data["text"] = message.text
        await message.answer("📞 Теперь введи свой Telegram username (@user):")
        return

    # 3 шаг — контакт
    if "contact" not in data:
        data["contact"] = message.text

        post = (
            f"🆕 НОВОЕ ОБЪЯВЛЕНИЕ\n\n"
            f"📍 Город: {data['city']}\n\n"
            f"📝 {data['text']}\n\n"
            f"⭐ Контакт скрыт"
        )

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="⭐ Открыть контакт", callback_data=f"open_{uid}")]
        ])

        # отправка в группу (без контакта)
        await bot.send_message(GROUP_ID, post, reply_markup=keyboard)

        await message.answer("✅ Объявление опубликовано!")

        # сохраняем данные (контакт НЕ показываем в группе)
        await message.answer("💎 Контакт скрыт и доступен за Stars ⭐")

# ---------------- ОТКРЫТИЕ КОНТАКТА ----------------
@dp.callback_query(F.data.startswith("open_"))
async def open_contact(callback: types.CallbackQuery):
    uid = int(callback.data.split("_")[1])

    if uid not in ads:
        await callback.message.answer("❌ Объявление не найдено")
        return

    contact = ads[uid]["contact"]

    # ⚠️ пока заглушка Stars
    await callback.message.answer(
        f"💳 После оплаты Stars ⭐ будет открыт контакт:\n\n"
        f"📞 {contact}"
    )

# ---------------- RUN ----------------
async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
