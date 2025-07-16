import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackContext, 
    CallbackQueryHandler, MessageHandler, Filters
)
import re
import os

# Configuration (using your bot token directly as requested)
TOKEN = "7876986178:AAEEAwCohyMjusSikwAAIKfCOWzEy-7dgoo"
TWITTER_URL = "https://twitter.com/jkvnjkvnjv"
FACEBOOK_URL = "https://facebook.com/viwvwvwnivnv"

# User states
(START, AWAIT_ADDRESS) = range(2)
user_data = {}

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# SOLANA ADDRESS VALIDATION
def is_valid_solana_address(address: str) -> bool:
    return re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", address) is not None

# Start Command
def start(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_data[user_id] = {"completed": False}
    
    keyboard = [
        [
            InlineKeyboardButton("Join Telegram Channel", url="https://t.me/your_channel"),
            InlineKeyboardButton("Join Telegram Group", url="https://t.me/your_group")
        ],
        [
            InlineKeyboardButton("Follow Twitter", url=TWITTER_URL),
            InlineKeyboardButton("Follow Facebook", url=FACEBOOK_URL)
        ],
        [InlineKeyboardButton("✅ I've Completed All Steps", callback_data="complete")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "🌟 Welcome to the Oliwest Airdrop! 🌟\n\n"
        "To qualify for 100 SOL airdrop:\n"
        "1. Join our Telegram Channel\n"
        "2. Join our Telegram Group\n"
        "3. Follow us on Twitter\n"
        "4. Follow us on Facebook\n\n"
        "Complete all steps and click the confirmation:",
        reply_markup=reply_markup
    )
    
    return START

# Completion Handler
def complete(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    user_data[user_id]["completed"] = True
    
    query.edit_message_text(
        "👍 Well done! Hope you didn't cheat the system!\n\n"
        "Please send your Solana wallet address now:"
    )
    
    return AWAIT_ADDRESS

# Handle Solana Address Submission
def handle_address(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    address = update.message.text.strip()
    
    if not user_data.get(user_id, {}).get("completed"):
        update.message.reply_text("❌ Please complete all steps first using /start")
        return START
    
    if is_valid_solana_address(address):
        update.message.reply_text(
            "🎉 Congratulations! You've passed the Oliwest Airdrop call!\n\n"
            "100 SOL will be sent to your wallet:\n"
            f"`{address}`\n\n"
            "Thank you for participating!",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    else:
        update.message.reply_text("❌ Invalid Solana address. Please send a valid address:")
        return AWAIT_ADDRESS

# Cancel Handler
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Action cancelled.')
    return ConversationHandler.END

# Error Handler
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f"Update {update} caused error {context.error}")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [CallbackQueryHandler(complete, pattern='^complete$')],
            AWAIT_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, handle_address)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
