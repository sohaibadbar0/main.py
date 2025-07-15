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
)
import logging
import os

BOT_TOKEN = "7783908047:AAF9KwNaCkhXPNw2SFRPD8y2KwfmwJDkJg0"

logging.basicConfig(level=logging.INFO)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Launch Mini Game", url="https://t.me/Pandooverse_bot/Pandooverse")],
        [InlineKeyboardButton("🖼 Show Random NFT", callback_data='random_nft')],
        [InlineKeyboardButton("🌐 Explore Links", callback_data='show_links')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎉 Welcome to *PANDOO-VERSE*!", reply_markup=reply_markup, parse_mode="Markdown")

# === /help ===
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 *Available Commands:*\n\n"
        "/start - Show menu\n"
        "/help - Show this help message\n"
        "/about - About the Pandoo-Verse project\n"
        "/links - Quick access to platforms\n"
        "/nft <token> - View NFT metadata\n"
        "/price <collection> - Check floor price"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# === /about ===
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐼 *PANDOO-VERSE* is a panda-themed NFT world of stories, games, and collectibles.\n"
        "🌐 Explore more: https://pandooverse.x.rarible.com/",
        parse_mode="Markdown"
    )

# === /links ===
async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌐 Website", url="https://pandooverse.x.rarible.com/")],
        [InlineKeyboardButton("📦 OpenSea", url="https://opensea.io/collection/pandooverse")],
        [InlineKeyboardButton("🧙 Magic Eden", url="https://magiceden.io/u/BambooLabs")],
        [InlineKeyboardButton("🖼 Rarible", url="https://rarible.com/pandoo-verse")]
    ]
    await update.message.reply_text("🔗 Explore more:", reply_markup=InlineKeyboardMarkup(keyboard))

# === /nft <token_id> (metadata placeholder) ===
async def nft_metadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗Usage: `/nft <token_id>`", parse_mode="Markdown")
        return

    token_id = context.args[0]
    await update.message.reply_text(
        f"🔍 Fetching metadata for token ID: `{token_id}`...\n\n"
        "👉 (Metadata feature coming soon!)",
        parse_mode="Markdown"
    )

# === /price <collection_name> (price placeholder) ===
async def price_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗Usage: `/price <collection>`", parse_mode="Markdown")
        return

    collection = context.args[0]
    await update.message.reply_text(
        f"💰 Checking floor price for `{collection}`...\n\n"
        "👉 (Live tracking in next phase!)",
        parse_mode="Markdown"
    )

# === Callback handler (buttons) ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_links":
        await links(query, context)
    elif query.data == "random_nft":
        await query.message.reply_photo(
            photo="https://ipfs.raribleuserdata.com/ipfs/bafybeica5pnqglknw52frn36tfdvydnp7llpohz7x5lqmpys2ll3fhtk34/image.png",
            caption="🧸 *PLAYER 456*\n💥 *Mood:* REVENGE SEEKING\n\n🛒 *Buy on:*\n- [OpenSea](https://opensea.io/collection/pandooverse)",
            parse_mode="Markdown"
        )

# === Set visible commands ===
async def set_bot_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Show main menu"),
        BotCommand("help", "Show help"),
        BotCommand("about", "About the project"),
        BotCommand("links", "NFT marketplace links"),
        BotCommand("nft", "View NFT metadata by token ID"),
        BotCommand("price", "Check floor price by collection name"),
    ])

# === Main ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("nft", nft_metadata))
    app.add_handler(CommandHandler("price", price_check))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.post_init = set_bot_commands  # ⬅️ Registers commands on Telegram

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
