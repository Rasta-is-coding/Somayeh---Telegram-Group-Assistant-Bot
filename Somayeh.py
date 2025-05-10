from typing import Final
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import logging
import random


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8'  # for UnicodeEncodeError
)
logger = logging.getLogger(__name__)


TOKEN: Final = 'BLA BLA BLA'
BOT_USERNAME: Final = '@somayeh_iut_bot'

# Command for "/start"
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received /start command")
    await update.message.reply_text('سمیه در خدمت گذاری حاضره')

# responses 
def calling_Somayeh(text: str) -> str:
    processed: str = text.lower().strip()
    logger.info(f"Processing message: {processed}")  # Debugging line

    rand_responses = [
        "جونم؟",
        "ها؟",
        "دیگه چته؟",
        "چته؟",
        "بنال",
        "سمیه و درد بی درمون"
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
        return 'سلام خدمت اهالی خفن گروه تحقیقاتی حکیم گستران'
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

    message_type: str = update.message.chat.type
    text: str = update.message.text


    logger.info(f'User ({update.message.chat.id}) in {message_type} says: {text}')


    is_reply_to_bot = (
        update.message.reply_to_message is not None and
        update.message.reply_to_message.from_user.id == context.bot.id
    )


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
            # cleaning from the start to end
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

            #deleting the cleaning message
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




    # Check if message contains "سمیه"
    if message_type == 'group':
        if 'سمیه' in text or is_reply_to_bot:
            respond = calling_Somayeh(text)
            await update.message.reply_text(respond)

        else:
            print("Message does not contain 'سمیه' in group")
            return
    else:
        respond: str = calling_Somayeh(text)
        await update.message.reply_text(respond)

# Error handler
async def error(update: Update, context: ContextTypes.context):
    logger.error(f"Update: {update} caused error: {context.error}")


# Main block to run the bot
if __name__ ==  '__main__':
    print('Starting bot')
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler('start', start_command))  # Start command handler
    app.add_handler(MessageHandler(filters.TEXT, message_handle))  # Message handler
    
    # Error handler
    app.add_error_handler(error)

    print('Bot is polling')
    app.run_polling(poll_interval=1)



