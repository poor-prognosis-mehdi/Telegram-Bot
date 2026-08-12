import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request, jsonify
import os

TOKEN = "7767860852:AAFdsGfjaKv_UhaT4t3fl2J742WDxYWh804"
ADMIN_ID = 218104646

# برای ذخیره وضعیت موقت (بعداً باید به دیتابیس تغییر کنه)
waiting_users = {}

# ساخت اپلیکیشن Flask
app = Flask(__name__)

# ساخت ربات
bot = telebot.TeleBot(TOKEN)

# ----------------- هندلرهای ربات (بدون تغییر) -----------------

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    btn_telegram = InlineKeyboardButton("📱 ارتباط با من", url="https://t.me/poor_prognosis_mehdi")
    btn_card = InlineKeyboardButton("🪪 مشاهده کارت", url="https://linktr.ee/mohammadmehdidaghighian")
    btn_question = InlineKeyboardButton("✉️ پیام شخصی", callback_data="ask_question")
    markup.add(btn_telegram)
    markup.add(btn_card)
    markup.add(btn_question)
    bot.send_message(message.chat.id, "یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "ask_question")
def ask_question(call):
    user_id = call.from_user.id
    waiting_users[user_id] = True
    bot.send_message(user_id, "سوال خود را بنویس و ارسال کن:")

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
    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ سوال شما با موفقیت ارسال شد.")
    del waiting_users[user.id]

# ----------------- بخش سرورلس (Flask) -----------------

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    این تابع هر بار که تلگرام پیام جدید می‌فرسته، صدا زده میشه.
    """
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'error'}), 403

# این تابع مخصوص پلتفرم‌هایی مثل Vercel یا AWS Lambda هست
def main(event, context):
    # وقتی پلتفرم سرورلس درخواست رو میاره، میندازه توی Flask
    with app.test_client() as client:
        response = client.post(
            '/webhook',
            data=event.get('body', ''),
            headers={
                'Content-Type': event.get('headers', {}).get('Content-Type', 'application/json')
            }
        )
        return {'statusCode': response.status_code, 'body': response.get_data(as_text=True)}
