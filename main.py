from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.filters import Command
from config import TOKEN
import asyncio
import json
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

STATE_FILE = BASE_DIR / "state.json"

bot = Bot(TOKEN)
dp = Dispatcher()
current_user_id = None
current_user_name = None
reminder_task = None
enter_button = InlineKeyboardButton(
    text="🟢 Увійти в банк",
    callback_data="enter",
)
exit_button = InlineKeyboardButton(
    text="🔴 Вийти з банку",
    callback_data="exit",
)
enter_keyboard = InlineKeyboardMarkup(inline_keyboard=[[enter_button]])
exit_keyboard = InlineKeyboardMarkup(inline_keyboard=[[exit_button]])


def save_state():
    data = {
        "current_user_id": current_user_id,
        "current_user_name": current_user_name,
    }

    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def load_state():
    global current_user_id, current_user_name

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        current_user_id = data["current_user_id"]
        current_user_name = data["current_user_name"]

    except FileNotFoundError:
        pass


async def bank_reminder(message: Message):
    await asyncio.sleep(15 * 60)

    await message.edit_text(
        f"⏰ У банку понад 15 хвилин: {current_user_name}",
        reply_markup=exit_keyboard,
    )


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привіт! Я бот обліку банку.",
        reply_markup=enter_keyboard,
    )


@dp.callback_query(F.data == "enter")
async def enter(callback: CallbackQuery):
    global current_user_id, current_user_name, reminder_task

    if current_user_id is None:
        current_user_id = callback.from_user.id
        current_user_name = callback.from_user.full_name

        save_state()

        await callback.message.edit_text(
            f"🔴 У банку: {callback.from_user.full_name}",
            reply_markup=exit_keyboard,
        )

        reminder_task = asyncio.create_task(bank_reminder(callback.message))

    else:
        await callback.answer(
            f"🔴 Банк вже зайнятий. Зараз у банку: {current_user_name}",
            show_alert=True,
        )


@dp.callback_query(F.data == "exit")
async def exit(callback: CallbackQuery):
    global current_user_id, current_user_name, reminder_task

    if callback.from_user.id == current_user_id:
        await callback.message.edit_text(
            "🟢 Банк вільний",
            reply_markup=enter_keyboard,
        )

        current_user_id = None
        current_user_name = None

        save_state()

        if reminder_task is not None:
            reminder_task.cancel()
            reminder_task = None
    else:
        await callback.answer(
            "❌ Ви не можете вийти з банку замість іншого користувача.",
            show_alert=True,
        )


@dp.message(Command("reset"))
async def reset(message: Message):
    global current_user_id, current_user_name, reminder_task

    if reminder_task is not None:
        reminder_task.cancel()
        reminder_task = None

    current_user_id = None
    current_user_name = None

    save_state()

    await message.answer(
        "🟢 Банк вільний",
        reply_markup=enter_keyboard,
    )


async def main():
    await dp.start_polling(bot)


load_state()

asyncio.run(main())
