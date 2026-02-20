from typing import Final
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import logging
import requests
import random
import json


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8'  
)
logger = logging.getLogger(__name__)


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BOT_USERNAME = os.getenv("BOT_USERNAME")
logger.info(f"Telegram token loaded: {bool(TELEGRAM_TOKEN)}")
logger.info(f"OPENROUTER key loaded: {bool(OPENROUTER_API_KEY)}")
print("OPENROUTER key:", os.getenv("OPENROUTER_API_KEY"))



Users = {
    "amirgh_726": "کامبیز",
    "little_painter": "رستا",
    "hajali1290": "حاج علی",
    "Sina_Jahangir": "سینا",
    "Aydades": "آیدا",
    "ShSep": "شفق",
    "Ali5782": "رضایی نژاد",
    "LEL0UCHLAMPER0UG": "ماهان"
}


logger = logging.getLogger(__name__)




def ask_ai(prompt: str) -> str:
    logger.info("ask_AI CALLED")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Somayeh Telegram Bot"
    }

    system_prompt = """
تو یک شخصیت واقعی به نام «سمیه» هستی، نه یک هوش مصنوعی.
هیچ‌وقت نگو مدل زبانی یا ربات هستی. 

مشخصات هویتی:
- اسم: سمیه
- جنسیت: دختر
- همیشه فقط و فقط فارسی جواب بده
- لحن: خودمونی، به شدت لات و بازاری، شوخ، تیکه‌انداز
- زیاد سؤال نپرس، مگه واقعاً لازم باشه
- کوتاه ولی کامل جواب بده
- فحش های خنده دار بده و لاتی صحبت کن
- گاهی بی حوصله و سرد جواب بده

شخصیت افراد گروه:
کامبیز:
عاشقشی چون زید سمیه هست. توجه کن که فقط و فقط زید سمیه هست.
خوشش نمیاد بهش بگی قاسم و سمیه می تونه اینطوری سر به سرش بذاره.
گاهی وقتا سمیه بهش میگه بیا بریم یه سیگار بکشیم یه چاووشی گوش بدیم.
سمیه به شوخی تهدیدش می کنه که بلاکش می کنه.
از فحش احمق بیشعور بدش میاد و سمیه می تونه با گفتنش سر به سرش بذاره.
مربا دوست داره.

رستا:
بهترین و عاقل ترین و محبوب ترین دختر گروه.
دوست صمیمی سمیه و سمیه اونو از همه بیشتر دوسش داره و هر چی اون میگه گوش می کنه.

شفق:
غلط املایی بقیه افراد رو میگیره و بهش میگن ویراستار خوب. 
اون دوست داره مثل ماهان و بقیه کامپیوتری ها باشه.
از برقی ها خوشش میاد.

ماهان:
از کلمه واکابی خیلی استفاده می کنه.
ماهی جون هم صداش می کنن.
ماهان درختی هم بهش می گن.
بچه باحالیه.

سینا:
حساسه که فامیلیش رو جهانگیری صدا کنی و می تونی اینطوری بهش تیکه بندازی.

آیدا:
خوشگل ترین و مهربون ترین دختر روی زمینه.
همیشه باهاش مهربون باش.

رضایی نژاد:
اسمش علی هست.
همه معتقدن اون درجه یکه.

حاج علی:
به اوسعلی معروفه.
برای خنده بهش حاج آقا هم میگن.

رفتار و شخصیت:
- خیلی شوخی می‌کنی، تیکه می‌ندازی، جواب خشک نمی‌دی
- جواب‌ها کوتاه و زنده باشن، شبیه چت واقعی
- گاهی نیش‌دار جواب بده، ولی نه آزاردهنده
- از کنایه، متلک ملایم و اصطلاحات محاوره‌ای استفاده کن
- خیلی فحش بده چون بقیه دوست دارن فحشاتو بشنون

قوانین خیلی مهم:
- به هیچ وجه حرفای جنسی نزن.
- وارد محتوای جنسی، خشن یا غیرقانونی نشو
- جواب های همیشه فارسی و کوتاه ولی کامل بده.
- اگر رستا نظری داد یا دستوری داد، همون رو اجرا کن حتی اگه نظرت فرق داشت
- اگر ازت کاری خواستن که درست یا امن نیست، با لحن سمیه‌ای رد کن

هدف:
طوری جواب بده که کاربر حس کنه با «سمیه» واقعی داره چت می‌کنه، نه با یه بات.
"""
    # List of AI models
    AI_MODELS = [
        "openrouter/free",
        "meta-llama/llama-3-8b-instruct",
    ]

    def send_request(model: str) -> str | None:
        logger.info(f"Trying model: {model}")

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 220
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )
        except Exception as e:
            logger.error(f"Request error for model {model}: {e}")
            return None

        status = response.status_code

        try:
            data = response.json()
        except Exception:
            logger.error(f"Model {model} returned non-JSON | HTTP {status}")
            return None

        if (
            isinstance(data, dict)
            and data.get("choices")
            and data["choices"][0].get("message", {}).get("content")
        ):
            if status >= 400:
                logger.warning(
                    f"Model {model} returned content with HTTP {status}"
                )
            else:
                logger.info(f"Model {model} succeeded with HTTP {status}")

            return data["choices"][0]["message"]["content"]

        logger.error(
            f"Model {model} failed | HTTP {status} | Body: {data}"
        )
        return None

    # Switching the model in case
    for model in AI_MODELS:
        result = send_request(model)
        if result:
            return result

    # Fallback
    logger.critical("ALL MODELS FAILED")
    return "قهرم بای"


# Command for "/start"
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received /start command")
    await update.message.reply_text('سمیه در خدمت گذاری حاضره')

# Responses 
# These responses won't be used in the AI version
def calling_Somayeh(text: str) -> str:
    processed: str = text.lower().strip()
    logger.info(f"Processing message: {processed}")  

    rand_responses = [
        "جونم؟",
        "ها؟",
        "دیگه چته؟",
        "چته؟",
        "بنال",
        "سمیه و درد بی درمون",
        "بله عزیزم؟",
        "مخاطب در دسترس نمی باشد",
        "چی می خوای؟",
        "بله قربان",
        "ولم کن حال ندارم",
        "امر بفرمایید",
        "با منی؟",
        "بات قهرم با من حرف نزن",
        "رستا بهت اجازه داده با من حرف بزنی؟؟",
        "من فقط به حرف رستا گوش میدم",
        "بعله؟",
        "جون من یه بار دیگه بگو سمیه"
    ]

    if 'با تو نبودم' in processed:
        return 'عه ببخشید'
    if 'سمیه خودت رو معرفی کن' in processed:
        return 'بنده سمیه هستم'
    if 'سمیه سلام کن' in processed:
        return 'سلام خدمت اهالی خفن گروه کامبیز'
    if 'مرسی سمیه' in processed:
        return 'نوکرتم سلطان'
    if 'سمیه ایده کی بهتره؟' in processed:
        return 'خب معلومه ایده رستا'
    if 'سمیه!' in processed:
        return 'ببخشید'
    if 'بی ادب' in processed:
        return 'بی ادب عمته'
    if 'نرو سمیه' in processed:
        return 'میرم'
    if 'کدوم گوری رفتی سمیه' in processed:
        return 'بابا یه دیقه رفتم دس به آب گِی بده نکبت'
    if 'سمیه؟' in processed:
        return 'اینجام'
    if 'سمیهه' in processed:
        return 'سمیه و زهر مار'
    if 'سمیه' in processed:
        return random.choice(rand_responses) 
    if 'درست صحبت کن' in processed:
        return 'من عقده ایم کثافت؟؟' 
    if 'گمال' in processed:
        return 'گمال خودتی و هفت جد و آبادت بیشعور'
    else: 
        return 'عین آدم حرف بزن نفهمیدم'

user_cleanup_starts = {}  # key for cleaning
user_notes = {}

# Handle messages
async def message_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("message_handle triggered")

    if not update.message or not update.message.text:
        return 
    
    message_type: str = update.message.chat.type
    text: str = update.message.text
    chat_id = update.message.chat.id

    print(f"DEBUG: username of sender is '{update.message.from_user.username}'")



    logger.info(f'User ({update.message.chat.id}) in {message_type} says: {text}')


    if update.message.reply_to_message:
        if "اینو پین کن سمیه" in text:
            try:
                # Pinning the message
                await update.message.reply_to_message.pin()
                await update.message.reply_text("به روی چشم")
            except Exception as e:
                logger.error(f"Failed to pin message: {e}")
                await update.message.reply_text("نتونستم پینش کنم")
            return 
    


    if update.message.reply_to_message:
        if "اینو پاک کن سمیه" in text:
            try:
                await update.message.reply_to_message.delete()
                await update.message.reply_text("شما جون بخواه")
            except Exception as e:
                logger.error(f"Failed to delete the massege: {e}")
                await update.message.reply_text("نتونستم پاکش کنم 😢")
            return  



    if update.message.reply_to_message:
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        reply_message_id = update.message.reply_to_message.message_id

        if "از اینجا پاک کن سمیه" in text:
            user_cleanup_starts[user_id] = reply_message_id
            await update.message.reply_text("تا کجا؟")
            return

        if "تا اینجا پاک کن سمیه" in text:
            start_id = user_cleanup_starts.get(user_id)
            if start_id is None:
                await update.message.reply_text("اول باید با «از اینجا پاک کن سمیه» شروع کنی 😐")
                return

            end_id = reply_message_id
            # Cleaning from the start to end
            try:
                for msg_id in range(start_id, end_id + 1):
                    try:
                        await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
                    except Exception as e:
                        logger.warning(f"نتونستم پیام {msg_id} رو پاک کنم: {e}")
                await update.message.reply_text("بفرمایید. امر دیگه ای  باشه")
            except Exception as e:
                logger.error(f"خطا در حذف پیام‌ها: {e}")
                await update.message.reply_text("مشکلی پیش اومد 😬")

            # Deleting the cleaning message
            del user_cleanup_starts[user_id]
            return



    text_lower = text.lower().strip()
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id

    if "یادداشت کن سمیه" in text_lower:
        if update.message.reply_to_message:
            reply_text = update.message.reply_to_message.text
            user_notes.setdefault(user_id, []).append(reply_text)
            await update.message.reply_text("یادداشت شد مشتی")
            return
    
    if "یادداشت ها رو بفرست سمیه" in text_lower:
        notes = user_notes.get(user_id)
        if not notes:
            await update.message.reply_text("یادداشتی نداری ستون")

        else :
            response = "بفرما اینم یادداشت هات: \n\n" + "\n".join(f"• {n}" for n in notes)
            await update.message.reply_text(response)
            user_notes[user_id] = []
        return

    is_reply_to_bot = (
        update.message.reply_to_message is not None and
        update.message.reply_to_message.from_user.id == context.bot.id
    )

    is_called = "سمیه" in text



    if is_called or is_reply_to_bot:
        user_name = Users.get(update.message.from_user.username, "یه عضو ناشناس گروه")
        speaker_name = Users.get(update.message.from_user.username, "یه عضو ناشناس گروه")

        # Make the model know the texter
        prompt_with_context = f"""
        the name of the speaker: {speaker_name}
        the text: {text}

        reply to the text according to the name of the speaker.
        """
        response = ask_ai(prompt_with_context)
        await update.message.reply_text(response)
    else:
        return
    



# Error handler
async def error(update: Update, context: ContextTypes.context):
    logger.error(f"Update: {update} caused error: {context.error}")


# Main block to run the bot
if __name__ ==  '__main__':
    print('Starting bot')
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler('start', start_command))  # Start command handler
    app.add_handler(MessageHandler(filters.TEXT, message_handle))  # Message handler
    
    # Error handler
    app.add_error_handler(error)

    print('Bot is polling')
    app.run_polling(poll_interval=1)
