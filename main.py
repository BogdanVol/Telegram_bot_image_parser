from enum import Enum

import constants as keys
from telegram.ext import *
import responses as R
from tesseract import tess
from telegram import *
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

print("Bot started...")


class Languages(Enum):
    ENG = 'eng'
    UA = 'ukr'


class LangManager:
    current_lang = Languages.UA


def create_buttons(update: Update, context: CallbackContext) -> None:
    name = update.message.chat.first_name
    update.message.reply_text("Hello " + name)
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='1')
        ],
        [
            InlineKeyboardButton("Українська", callback_data='2')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please chose language:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == '1':
        query.edit_message_text("Current language - English")
        LangManager.current_lang = Languages.ENG
    elif query.data == '2':
        query.edit_message_text("Поточна мова - Українська")
        LangManager.current_lang = Languages.UA

    update.message.reply_text("Send me photo")


def help_command(update, context):
    update.message.reply_text("Help yourself own")


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)
    update.message.reply_text(response, )


def image_handler(update, context):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    temp = obj.download()
    update.message.reply_text("Wait...")
    file_te = tess(temp, LangManager.current_lang.value)
    update.message.reply_text(file_te)


def error(update, context):
    print(f"Update {update} cause error {context.error}")


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", create_buttons))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)
    dp.add_handler(MessageHandler(Filters.photo, image_handler))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


main()
