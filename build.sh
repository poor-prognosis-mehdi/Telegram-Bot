#!/bin/bash
# این فایل بعد از هر بار آپلود کد، اجرا میشه و وب‌هوک رو ست می‌کنه
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=${RENDER_EXTERNAL_URL}/webhook"
