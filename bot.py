import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ContextTypes,
    CallbackQueryHandler, MessageHandler, filters
)
import re

# Configuration
TOKEN = "7876986178:AAEEAwCohyMjusSikwAAIKfCOWzEy-7dgoo"
TWITTER_URL = "https://twitter.com/jkvnjkvnjv"
FACEBOOK_URL = "https://facebook.com/viwvwvwnivnv"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# SOLANA ADDRESS VALIDATION
def is_valid_solana_address(address: str) -> bool:
    return re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", address) is not None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    
    await update.message.reply_text(
        "🌟 Welcome to the Oliwest Airdrop! 🌟\n\n"
        "To qualify for 100 SOL airdrop:\n"
        "1. Join our Telegram Channel\n"
        "2. Join our Telegram Group\n"
        "3. Follow us on Twitter\n"
        "4. Follow us on Facebook\n\n"
        "Complete all steps and click the confirmation:",
        reply_markup=reply_markup
    )

async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "👍 Well done! Hope you didn't cheat the system!\n\n"
        "Please send your Solana wallet address now:"
    )

async def handle_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    address = update.message.text.strip()
    
    if is_valid_solana_address(address):
        await update.message.reply_text(
            "🎉 Congratulations! You've passed the Oliwest Airdrop call!\n\n"
            "100 SOL will be sent to your wallet:\n"
            f"`{address}`\n\n"
            "Thank you for participating!",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("❌ Invalid Solana address. Please send a valid address:")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(complete, pattern="^complete$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_address))
    
    application.run_polling()

if __name__ == '__main__':
    main()
