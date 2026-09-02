import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN ="7767860852:AAHq5WqZ5ETffXQY671t9Adxkf_-33qu_6o"
ADMIN_ID = 218104646

ABOUT_ME_TEXT = """سلام دوست عزیز 👋

من محمد مهدی دقیقیان هستم؛ دانش‌آموخته کارشناسی علوم آزمایشگاهی از دانشگاه علوم پزشکی جندی‌شاپور اهواز و هم‌اکنون دانشجوی کارشناسی ارشد ویروس‌شناسی پزشکی دانشگاه علوم پزشکی جندی‌شاپور اهواز هستم.

خیلی خوشحال می‌شم که در قسمت «پیام شخصی» هر سوالی درباره بیماری‌های ویروسی که نیاز داری راجع‌بهشون اطلاعات داشته باشی، ازم بپرسی. من هم خوشحال می‌شم که به اندازه سوادی که دارم، سوالاتت رو اگه بلد باشم بهت جواب بدم.

یه سری بیماری‌های ویروسی خیلی شایع در جهان (STD) وجود دارن که خیلی خوبه درمورد راه‌های انتقال، بیماری‌زایی و شیوع‌شون اطلاع داشته باشی، و این بهت کمک می‌کنه تا سلامت بدنت رو تضمین کنی.

پس هر سوالی داشتی که خجالت می‌کشی بگی، می‌تونی به‌صورت پنهانی در قسمت «پیام شخصی» ازم بپرسی."""

STD_TESTS_TEXT = """🧪 تست‌های مربوط به بیماری‌های مقاربتی (جنسی)

🔹 تست‌های HPV:
HPV DNA / PAP Smear

🔹 تست‌های HIV:
HIV Ag/Ab, P24 / HIV PCR / Western Blot

🔹 تست‌های HBV:
HBsAg / HBV DNA Test"""

waiting_users = {}
question_map = {}  # کد سوال -> آیدی عددی کاربر
next_question_id = 1
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()

    btn_about = InlineKeyboardButton("👤 درباره من", callback_data="about_me")
    btn_telegram = InlineKeyboardButton("📱 ارتباط با من", url="https://t.me/poor_prognosis_mehdi")
    btn_card = InlineKeyboardButton("🪪 مشاهده کارت", url="https://linktr.ee/mohammadmehdidaghighian")
    btn_question = InlineKeyboardButton("✉️ پیام شخصی", callback_data="ask_question")

    btn_hpv = InlineKeyboardButton("HPV", url="https://youtu.be/pyihsgc209Q?si=LndSEasvzrDPtw33")
    btn_hiv = InlineKeyboardButton("HIV", url="https://youtu.be/OQnX8u9Y6e0?si=VxWfXW1Yy58pBXa-")
    btn_hbv = InlineKeyboardButton("HBV", url="https://youtu.be/0jrHRv2pJXQ?si=O9cSCQfYP6szW3qT")
    btn_hsv = InlineKeyboardButton("HSV", url="https://youtu.be/PaLu2K18jpk?si=oKhJjetv6jhKupoh")
    btn_tests = InlineKeyboardButton("🧪 تست‌های مربوط به بیماری‌های مقاربتی(جنسی)", callback_data="std_tests")
    btn_sites = InlineKeyboardButton("🌐 سایت‌های معتبر علمی/پزشکی", callback_data="trusted_sites")

    # ترتیب ردیف‌ها دقیقاً همین‌طور که چیده شده رندر می‌شود
    markup.row(btn_about)
    markup.row(btn_telegram)
    markup.row(btn_card)
    markup.row(btn_question)
    markup.row(btn_hpv, btn_hiv)
    markup.row(btn_hbv, btn_hsv)
    markup.row(btn_tests)
    markup.row(btn_sites)

    bot.send_message(message.chat.id, "یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "about_me")
def about_me(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, ABOUT_ME_TEXT)

@bot.callback_query_handler(func=lambda call: call.data == "trusted_sites")
def trusted_sites(call):
    bot.answer_callback_query(call.id)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🇺🇸 CDC", url="https://www.cdc.gov/std/"))
    markup.row(InlineKeyboardButton("🌍 WHO", url="https://www.who.int/health-topics/sexually-transmitted-infections"))
    markup.row(InlineKeyboardButton("🏥 Mayo Clinic", url="https://www.mayoclinic.org/diseases-conditions/sexually-transmitted-diseases-stds/symptoms-causes/syc-20351240"))
    bot.send_message(
        call.message.chat.id,
        "🌐 برای اطلاعات علمی و معتبر می‌تونی به این سایت‌ها مراجعه کنی:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "std_tests")
def std_tests(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, STD_TESTS_TEXT)

@bot.callback_query_handler(func=lambda call: call.data == "ask_question")
def ask_question(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    waiting_users[user_id] = True
    bot.send_message(user_id, "سوال خود را بنویس و ارسال کن:")

@bot.message_handler(func=lambda message: message.from_user.id in waiting_users)
def receive_question(message):
    global next_question_id
    user = message.from_user

    qid = next_question_id
    next_question_id += 1
    question_map[qid] = user.id

    text = f"""
📩 سوال جدید دریافت شد (ناشناس)
🔑 کد سوال: {qid}
💬 متن سوال:
{message.text}

↩️ برای پاسخ، این دستور را بفرست:
/reply {qid} متن پاسخ شما
"""
    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "✅ سوال شما با موفقیت ارسال شد.")
    del waiting_users[user.id]

@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    if message.from_user.id != ADMIN_ID:
        return  # فقط ادمین اجازه پاسخ دادن دارد

    try:
        parts = message.text.split(maxsplit=2)
        qid = int(parts[1])
        answer_text = parts[2]
    except (IndexError, ValueError):
        bot.send_message(ADMIN_ID, "❌ فرمت درست: /reply کد متن‌پاسخ")
        return

    target_user_id = question_map.get(qid)
    if not target_user_id:
        bot.send_message(ADMIN_ID, "❌ کد سوال معتبر نیست یا قبلاً پاسخ داده شده.")
        return

    try:
        bot.send_message(target_user_id, f"📬 پاسخ به سوال شما:\n\n{answer_text}")
        bot.send_message(ADMIN_ID, "✅ پاسخ ارسال شد.")
        del question_map[qid]
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ ارسال پاسخ ناموفق بود: {e}")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
