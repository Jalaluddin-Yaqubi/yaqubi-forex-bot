
import logging
import requests
import time
from datetime import datetime
from telegram import Bot
import pytz

# --- تنظیمات ---
TOKEN = '7513317675:AAHicsTAqwBqxF5FuDXKYo8b1OKXg3Gb3ts'
CHANNEL_ID = '@Yaqubi_Forex_Signals'
TIMEZONE = 'Asia/Kabul'
IMPACT_LEVELS = ['High', 'Medium']
CHECK_INTERVAL = 300  # هر ۵ دقیقه

# --- تنظیمات لاگ ---
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)

# --- تابع تبدیل زمان ---
def local_time(utc_str):
    utc_time = datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%SZ')
    local = pytz.utc.localize(utc_time).astimezone(pytz.timezone(TIMEZONE))
    return local.strftime('%Y-%m-%d - %H:%M')

# --- تابع دریافت اخبار ---
def fetch_news():
    try:
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        res = requests.get(url)
        data = res.json()
        return data
    except:
        return []

# --- تابع تحلیل خبر ---
def analyze_impact(event):
    impact = event.get("impact", "")
    if impact == "High":
        return "📈"
    elif impact == "Medium":
        return "📉"
    return ""

# --- ارسال خبر به کانال ---
def send_news(event):
    title = event.get("title", "")
    country = event.get("country", "")
    date = local_time(event.get("date", ""))
    impact = event.get("impact", "")
    actual = event.get("actual", "N/A")
    forecast = event.get("forecast", "N/A")
    previous = event.get("previous", "N/A")
    symbol = analyze_impact(event)

    message = f"""
📢 خبر اقتصادی جدید

📅 تاریخ: {date}
🌍 کشور: {country}
📰 عنوان: {title}
⚡ اهمیت: {impact}
📊 مقدار واقعی: {actual}
📈 پیش‌بینی: {forecast}
📉 مقدار قبلی: {previous}

{symbol} تحلیل: بر بازار تاثیر خواهد داشت
"""
    bot.send_message(chat_id=CHANNEL_ID, text=message.strip())

# --- اجرای اصلی ---
def main():
    sent_ids = set()
    while True:
        logging.info("در حال بررسی اخبار اقتصادی...")
        news_list = fetch_news()
        for news in news_list:
            news_id = news.get("id")
            if news_id not in sent_ids and news.get("impact") in IMPACT_LEVELS:
                send_news(news)
                sent_ids.add(news_id)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
