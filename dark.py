from telethon import TelegramClient, events
import logging
import re

# معلومات API من my.telegram.org
API_ID = 29252624  # استبدل بـ API_ID الخاص بك
API_HASH = 'a2d8bc6c8298b8b7dd31ba065ede8266'  # استبدل بـ API_HASH الخاص بك

# معلومات القنوات
TARGET_CHANNELS = [
    '@khalil124kh',  # القناة الأولى
    '@idlib_marsad',  # القناة الثانية
    '@forat_syria',  # القناة الثالثة
    '@NeWSALMHARAR',  # القناة الرابعة
    '@my_dark2',  # القناة الخامسة
]
YOUR_CHANNEL = '@Syria_8_12'  # قناتك

# نص التذييل
FOOTER_TEXT = "\n\nردع العدوان سوريا تليجرام : https://t.me/Syria_8_12"

# إعدادات التسجيل (Logging)
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء العميل
client = TelegramClient('session_name', API_ID, API_HASH)

# دالة لحذف الروابط من النص
def remove_links(text):
    # تعبير عادي للبحث عن الروابط
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub('', text).strip()

# دالة لنسخ الرسائل
@client.on(events.NewMessage(chats=TARGET_CHANNELS))
async def forward_message(event):
    try:
        # حذف الروابط من النص الأصلي
        cleaned_text = remove_links(event.text) if event.text else ""

        # إضافة التذييل إلى النص
        message_text = cleaned_text + FOOTER_TEXT

        # نسخ الرسالة إلى قناتك
        await client.send_message(YOUR_CHANNEL, message_text, file=event.media if event.media else None)
        logger.info(f"تم نسخ رسالة جديدة من {event.chat.username}: {cleaned_text if cleaned_text else 'رسالة تحتوي على ميديا'}")

    except Exception as e:
        logger.error(f"حدث خطأ أثناء نسخ الرسالة: {e}")

# بدء العميل
async def main():
    try:
        await client.start()
        logger.info("تم تسجيل الدخول بنجاح! البوت يعمل ويراقب القنوات المستهدفة...")
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"حدث خطأ أثناء تشغيل البوت: {e}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())