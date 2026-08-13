import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# توکن خود را اینجا قرار دهید
TOKEN = "7767860852:AAFTlW9PtNp22LA0HLK4Eksw2N1t_8vL2-c"
ADMIN_ID = 218104646

# برای ذخیره وضعیت موقت
waiting_users = {}

# ساخت ربات
bot = telebot.TeleBot(TOKEN)

# ----------------- هندلرهای ربات -----------------

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    btn_telegram = InlineKeyboardButton("📱 ارتباط با من", url="https://t.me/poor_prognosis_mehdi")
    btn_card = InlineKeyboardButton("🪪 مشاهده کارت", url="https://linktr.ee/mohammadmehdidaghighian")
    btn_about = InlineKeyboardButton("👤 درباره من", callback_data="about_me")
    btn_question = InlineKeyboardButton("✉️ پیام شخصی", callback_data="ask_question")
    
    markup.add(btn_telegram)
    markup.add(btn_card)
    markup.add(btn_about)
    markup.add(btn_question)
    
    bot.send_message(message.chat.id, "یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=markup)

# تابع مدیریت دکمه "درباره من"
@bot.callback_query_handler(func=lambda call: call.data == "about_me")
def about_me(call):
    # متن معرفی شما
    about_text = """
سلام دوست عزیز ،

من محمد مهدی دقیقیان هستم ؛ 
دانش آموخته کارشناسی علوم آزمایشگاهی از دانشگاه علوم پزشکی جندی شاپور اهواز و هم اکنون دانشجوی کارشناسی ارشد ویروس شناسی پزشکی دانشگاه علوم پزشکی جندی شاپور اهواز هستم ؛ 

خیلی خوشحال میشم که در قسمت پیام شخصی هر سوالی درباره بیماری های ویروسی که نیاز داری راجب شون اطلاعات داشته باشی ازم بپرسی من هم خوشحال میشم که به اندازه سوادی که دارم سوالات ات رو اگه بلد باشم بهت جواب بدم ؛ 

یه سری بیماری های ویروسی خیلی شایع در جهان(STD) وجود دارن که خیلی خوبه که درمورد راه های انتقال و بیماری زایی و شیوع شون اطلاع داشته باشی و این بهت کمک میکنه تا سلامت بدن ات رو تضمین کنی. 

پس هر سوالی داشتی که خجالت میکشی بگی میتونی به صورت پنهانی در قسمت پیام شخصی ازم بپرس.
"""
    # ارسال متن به کاربر
    bot.send_message(call.message.chat.id, about_text)
    # نمایش تیک تایید روی دکمه
    bot.answer_callback_query(call.id, text="در حال نمایش اطلاعات...")

@bot.callback_query_handler(func=lambda call: call.data == "ask_question")
def ask_question(call):
    user_id = call.from_user.id
    waiting_users[user_id] = True
    bot.send_message(user_id, "سوال خود را بنویس و ارسال کن:")

@bot.message_handler(func=lambda message: message.from_user.id in waiting_users)
def receive_question(message):
    # فقط متن پیام دریافت و برای ادمین ارسال می‌شود، بدون هیچ مشخصاتی از فرستنده
    text = f"""
📩 یک پیام شخصی جدید دریافت شد:

💬 متن پیام:
{message.text}
"""
    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ سوال شما با موفقیت ارسال شد.")
    del waiting_users[message.from_user.id]

# ----------------- اجرای بات روی VPS -----------------

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
