import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN ="7767860852:AAESRxOV-yR0QMoHi0XDR6p6BLqslfa-9Q0"
ADMIN_ID = 218104646

ABOUT_ME_TEXT = """سلام دوست عزیز 👋

من محمد مهدی دقیقیان هستم؛ دانش‌آموخته کارشناسی علوم آزمایشگاهی از دانشگاه علوم پزشکی جندی‌شاپور اهواز و هم‌اکنون دانشجوی کارشناسی ارشد ویروس‌شناسی پزشکی دانشگاه علوم پزشکی جندی‌شاپور اهواز هستم.

خیلی خوشحال می‌شم که در قسمت «پیام شخصی» هر سوالی درباره بیماری‌های ویروسی که نیاز داری راجع‌بهشون اطلاعات داشته باشی، ازم بپرسی. من هم خوشحال می‌شم که به اندازه سوادی که دارم، سوالاتت رو اگه بلد باشم بهت جواب بدم.

یه سری بیماری‌های ویروسی خیلی شایع در جهان (STD) وجود دارن که خیلی خوبه درمورد راه‌های انتقال، بیماری‌زایی و شیوع‌شون اطلاع داشته باشی، و این بهت کمک می‌کنه تا سلامت بدنت رو تضمین کنی.

پس هر سوالی داشتی که خجالت می‌کشی بگی، می‌تونی به‌صورت پنهانی در قسمت «پیام شخصی» ازم بپرسی."""

waiting_users = {}
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    btn_about = InlineKeyboardButton("👤 درباره من", callback_data="about_me")
    btn_telegram = InlineKeyboardButton("📱 ارتباط با من", url="https://t.me/poor_prognosis_mehdi")
    btn_card = InlineKeyboardButton("🪪 مشاهده کارت", url="https://linktr.ee/mohammadmehdidaghighian")
    btn_question = InlineKeyboardButton("✉️ پیام شخصی", callback_data="ask_question")
    markup.add(btn_about)
    markup.add(btn_telegram)
    markup.add(btn_card)
    markup.add(btn_question)
    bot.send_message(message.chat.id, "یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "about_me")
def about_me(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, ABOUT_ME_TEXT)

@bot.callback_query_handler(func=lambda call: call.data == "ask_question")
def ask_question(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    waiting_users[user_id] = True
    bot.send_message(user_id, "سوال خود را بنویس و ارسال کن:")

@bot.message_handler(func=lambda message: message.from_user.id in waiting_users)
def receive_question(message):
    user = message.from_user
    username = user.username if user.username else "ندارد"
    text = f"""
📩 سوال جدید دریافت شد
🆔 آیدی عددی: {user.id}
💬 متن سوال:
{message.text}
"""
    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ سوال شما با موفقیت ارسال شد.")
    del waiting_users[user.id]

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
