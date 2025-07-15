from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
import logging
import os

BOT_TOKEN = "7783908047:AAHyyd6kxXWHVo4kAulyKOJH5qjKWKuMHDs"
ADMIN_ID = 5395716154 # Replace with your Telegram user ID

user_ids = set()

logging.basicConfig(level=logging.INFO)

# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ids.add(update.effective_user.id)

    keyboard = [
        [InlineKeyboardButton("🎮 Launch Mini Game", url="https://t.me/Pandooverse_bot/Pandooverse")],
        [InlineKeyboardButton("📄 About Project", callback_data='about')],
        [InlineKeyboardButton("🌐 NFT Links", callback_data='show_links')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎉 Welcome to *PANDOO-VERSE*!", reply_markup=reply_markup, parse_mode="Markdown")

# ✅ /help command
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 *Available Commands:*\n\n"
        "/start - Show menu\n"
        "/help - List all commands\n"
        "/about - About the project\n"
        "/links - Explore NFT marketplaces\n"
        "/broadcast <msg> - Admin only: send message to all users"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# ✅ /about command
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "🐼 *PANDOO-VERSE* is a story-driven NFT collection featuring unique panda characters.\n\n"
        "🎯 Vision: Build a Web3 universe with storytelling, collectibles, games & community power.\n\n"
        "🔗 [Visit Collection](https://pandooverse.x.rarible.com/)"
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")

# ✅ /links command
async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌐 Website", url="https://pandooverse.x.rarible.com/")],
        [InlineKeyboardButton("📦 OpenSea", url="https://opensea.io/collection/pandooverse")],
        [InlineKeyboardButton("🧙 Magic Eden", url="https://magiceden.io/u/BambooLabs")],
        [InlineKeyboardButton("🖼 Rarible", url="https://rarible.com/pandoo-verse")],
        [InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/labsbambooo")],
        [InlineKeyboardButton("🐦 Twitter", url="https://x.com/GenesisDodo")],
        [InlineKeyboardButton("📢 Telegram Bot", url="https://t.me/Pandooverse_bot")],
    ]
    await update.message.reply_text("🔗 Explore more:", reply_markup=InlineKeyboardMarkup(keyboard))

# ✅ Broadcast command (admin only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not allowed to broadcast.")
        return

    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("❗Usage: /broadcast <your message>")
        return

    count = 0
    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 Broadcast:\n\n{msg}")
            count += 1
        except:
            continue
    await update.message.reply_text(f"✅ Sent to {count} users.")

# ✅ Callback handler for inline buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await about(query, context)
    elif query.data == "show_links":
        await links(query, context)

# ✅ Register bot commands
async def set_bot_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot and show menu"),
        BotCommand("help", "Show help menu"),
        BotCommand("about", "About the Pandoo-Verse"),
        BotCommand("links", "Explore collections"),
        BotCommand("broadcast", "Admin only"),
    ])

# ✅ Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.add_handler(CallbackQueryHandler(button_handler))

    app.post_init = set_bot_commands

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
