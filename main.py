import logging
import os
import random
import aiohttp
import asyncio
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# === Load environment variables ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
CONTRACT_ADDRESS = "0x25b9076dcd51f64ae556a40e3416fd1d4aabb730"

# === Logging ===
logging.basicConfig(level=logging.INFO)

NFT_IMAGES = [
    "https://ipfs.raribleuserdata.com/ipfs/bafybeica5pnqglknw52frn36tfdvydnp7llpohz7x5lqmpys2ll3fhtk34/image.png",
    "https://ipfs.raribleuserdata.com/ipfs/bafybeigbhbmuzhejjxiy3267j3fcgf33vxjoubwp6ipkdzwhmrxj6jpbsi/image.png",
]

# === Bot commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Launch Mini Game", url="https://t.me/Pandooverse_bot/Pandooverse")],
        [InlineKeyboardButton("🖼 Show Random NFT", callback_data='random_nft')],
        [InlineKeyboardButton("🌐 Explore Links", callback_data='show_links')],
    ]
    await update.message.reply_text("🎉 Welcome to *PANDOO-VERSE*!", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 *Available Commands:*\n"
        "/start - Show menu\n"
        "/nft <token_id> - View NFT metadata\n"
        "/price <slug> - Check floor price\n"
        "/about - Project info\n"
        "/links - Explore collection",
        parse_mode="Markdown"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🐼 *PANDOO-VERSE* is an NFT world of panda warriors and traits.\n🔗 https://pandooverse.x.rarible.com", parse_mode="Markdown")

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🌐 Website", url="https://pandooverse.x.rarible.com/")],
        [InlineKeyboardButton("📦 OpenSea", url="https://opensea.io/collection/pandooverse")],
        [InlineKeyboardButton("🧙 Magic Eden", url="https://magiceden.io/u/BambooLabs")],
        [InlineKeyboardButton("🖼 Rarible", url="https://rarible.com/pandoo-verse")],
    ]
    await update.message.reply_text("🔗 Links:", reply_markup=InlineKeyboardMarkup(buttons))

async def nft_metadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: `/nft <token_id>`", parse_mode="Markdown")
        return

    token_id = context.args[0]
    url = f"https://api.opensea.io/api/v2/chain/polygon/contract/{CONTRACT_ADDRESS}/nfts/{token_id}"
    headers = {"X-API-KEY": API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                await update.message.reply_text("❌ Couldn't fetch metadata.")
                return
            data = await resp.json()

    nft = data.get("nft", {})
    name = nft.get("name", "Unnamed")
    desc = nft.get("description", "No description.")
    image = nft.get("image_url", "")
    traits = nft.get("traits", [])
    trait_str = "\n".join([f"- *{t['trait_type']}*: {t['value']}" for t in traits]) if traits else "No traits."

    caption = f"🎨 *{name}*\n\n🖼 {desc}\n\n🎯 *Traits:*\n{trait_str}"
    await update.message.reply_photo(image, caption=caption, parse_mode="Markdown")

async def floor_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: `/price <slug>`", parse_mode="Markdown")
        return

    slug = context.args[0]
    url = f"https://api.opensea.io/api/v2/collections/{slug}/stats"
    headers = {"X-API-KEY": API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                await update.message.reply_text("🚫 API error or invalid slug.")
                return
            data = await resp.json()

    stats = data.get("total", {})
    floor = stats.get("floor_price", "N/A")
    volume = stats.get("total_volume", "N/A")
    await update.message.reply_text(f"📉 Floor Price: {floor}\n📈 Volume: {volume}", parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show_links":
        await links(query, context)
    elif query.data == "random_nft":
        image = random.choice(NFT_IMAGES)
        await query.message.reply_photo(image, caption="🎲 Here's a random NFT!", parse_mode="Markdown")

async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start bot"),
        BotCommand("help", "List commands"),
        BotCommand("about", "About Pandoo"),
        BotCommand("links", "View links"),
        BotCommand("nft", "Fetch NFT metadata"),
        BotCommand("price", "Check floor price"),
    ])

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("nft", nft_metadata))
    app.add_handler(CommandHandler("price", floor_price))
    app.add_handler(CallbackQueryHandler(button_handler))

    await set_commands(app)
    print("✅ Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
