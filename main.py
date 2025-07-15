from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, BotCommand 
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)
import random
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN") or "YOUR_BOT_TOKEN"

NFT_IMAGES = [
    "https://ipfs.raribleuserdata.com/ipfs/bafybeica5pnqglknw52frn36tfdvydnp7llpohz7x5lqmpys2ll3fhtk34/image.png",
    "https://ipfs.raribleuserdata.com/ipfs/bafybeigbhbmuzhejjxiy3267j3fcgf33vxjoubwp6ipkdzwhmrxj6jpbsi/image.png",
    "https://ipfs.raribleuserdata.com/ipfs/bafybeiacu4agkutieq7x6aaf7zr5fafqac5fyowjayzsgyyhy2r6vnzlda/image.png"
]

NFTS = [
    {
        "name": "ZOMBOO",
        "mood": "UNDEAD-VENGEANCE",
        "image": NFT_IMAGES[1],
        "links": {
            "OpenSea": "https://opensea.io/...",
            "Magic Eden": "https://magiceden.io/...",
            "Rarible": "https://rarible.com/...",
            "Official Site": "https://pandooverse.x.rarible.com/..."
        }
    },
    {
        "name": "PLAYER 456",
        "mood": "REVENGE SEEKING",
        "image": NFT_IMAGES[0],
        "links": {
            "OpenSea": "https://opensea.io/...",
            "Magic Eden": "https://magiceden.io/...",
            "Rarible": "https://rarible.com/...",
            "Official Site": "https://pandooverse.x.rarible.com/..."
        }
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Launch Mini Game", url="https://t.me/Pandooverse_bot/Pandooverse")],
        [InlineKeyboardButton("🖼 Show Random NFT", callback_data='random_nft')],
        [InlineKeyboardButton("🗂 Explore Collections", callback_data='show_links')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎉 Welcome to the PANDOO-VERSE Bot!", reply_markup=reply_markup)

async def random_nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    nft = random.choice(NFTS)
    links = "\n".join([f"- [{k}]({v})" for k, v in nft["links"].items()])

    caption = (
        f"🪄 Here's a random drop from the *PANDOO-VERSE!*\n\n"
        f"🧸 *{nft['name']}*\n"
        f"💥 *Mood:* {nft['mood']}\n\n"
        f"🛒 *Buy on:*\n{links}"
    )

    await query.message.reply_photo(
        photo=nft["image"],
        caption=caption,
        parse_mode="Markdown"
    )

async def show_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    links_text = (
        "🌐 Explore the PANDOO-VERSE Collections:\n"
        "- [OpenSea](https://opensea.io/collection/pandooverse)\n"
        "- [Magic Eden](https://magiceden.io/u/BambooLabs?chains=%5B%22polygon%22%5D)\n"
        "- [Rarible](https://pandooverse.x.rarible.com/)\n"
        "- [Official Site](https://pandooverse.x.rarible.com/)"
    )
    await query.message.reply_text(links_text, parse_mode='Markdown')


# 👇 INSERT HERE 👇 — Register commands for Telegram UI
async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot and view options"),
        BotCommand("info", "Show project info"),
        BotCommand("buy", "How to buy Pandoo NFTs")
    ])

# Main bot setup
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(random_nft, pattern="random_nft"))
    app.add_handler(CallbackQueryHandler(show_links, pattern="show_links"))

    app.post_init = set_commands  # ← ✅ Register commands

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
