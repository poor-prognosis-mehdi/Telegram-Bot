import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ["BOT_TOKEN"]  # از Environment Variable خونده می‌شه، نه هاردکد

bot = telebot.TeleBot(TOKEN)

# آیدی عددی خودت
ADMIN_ID = 218104646

# ذخیره وضعیت کاربران
waiting_users = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):

    markup = InlineKeyboardMarkup()

    btn_telegram = InlineKeyboardButton(
        "📱 ارتباط با من",
        url="https://t.me/poor_prognosis_mehdi"
    )

    btn_card = InlineKeyboardButton(
        "🪪 مشاهده کارت",
        url="https://linktr.ee/mohammadmehdidaghighian"
    )

    btn_question = InlineKeyboardButton(
        "✉️ پیام شخصی",
        callback_data="ask_question"
    )

    markup.add(btn_telegram)
    markup.add(btn_card)
    markup.add(btn_question)

    bot.send_message(
        message.chat.id,
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=markup
    )


# وقتی کاربر روی ارسال سوال کلیک کند
@bot.callback_query_handler(func=lambda call: call.data == "ask_question")
def ask_question(call):

    user_id = call.from_user.id

    waiting_users[user_id] = True

    bot.send_message(
        user_id,
        "سوال خود را بنویس و ارسال کن:"
    )


# دریافت پیام کاربر
@bot.message_handler(func=lambda message: message.from_user.id in waiting_users)
def receive_question(message):

    user = message.from_user

    username = user.username if user.username else "ندارد"

    text = f"""
📩 سوال جدید دریافت شد

👤 نام: {user.first_name}

🆔 آیدی عددی: {user.id}

🔹 یوزرنیم: @{username}

💬 متن سوال:

{message.text}
"""

    bot.send_message(
        ADMIN_ID,
        text
    )

    bot.send_message(
        message.chat.id,
        "✅ سوال شما با موفقیت ارسال شد."
    )

    del waiting_users[user.id]


print("Bot started...")
bot.infinity_polling()
