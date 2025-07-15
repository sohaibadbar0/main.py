import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Enable logging
logging.basicConfig(level=logging.INFO)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Launch Mini Game", url="https://t.me/Pandooverse_bot/Pandooverse")],
        [InlineKeyboardButton("🛒 Buy on OpenSea", url="https://opensea.io/collection/pandooverse")],
        [InlineKeyboardButton("🧙‍♂️ Buy on Magic Eden", url="https://magiceden.io/u/BambooLabs")],
        [InlineKeyboardButton("🖼 Buy on Rarible", url="https://rarible.com/pandoo-verse")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎉 Welcome to *PANDOO-VERSE*! Explore and shop your favorite NFTs.", reply_markup=reply_markup, parse_mode="Markdown")

# Set bot commands
async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Open main menu")
    ])

# Main function
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    await set_commands(app)

    print("✅ Bot is running...")
    await app.run_polling()

# Start bot
import asyncio
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
