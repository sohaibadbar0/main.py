logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Launch Mini Game", url="https://t.me/Pandooverse_bot/Pandooverse")],
        [InlineKeyboardButton("🖼 Show Random NFT", callback_data='random_nft')],
        [InlineKeyboardButton("🔗 Explore Links", callback_data='show_links')],
    ]
    await update.message.reply_text("🎉 Welcome to *PANDOO-VERSE*!", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *Available Commands:*\n"
        "/start - Show menu\n"
        "/nft <token_id> - View NFT metadata\n"
        "/price <slug> - Check floor price\n"
        "/about - Project info\n"
        "/links - Explore collection",
        parse_mode="Markdown"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🐼 *PANDOO-VERSE* is an NFT world of panda warriors and traits.\n🌐 https://pandooverse.x.rarible.com", parse_mode="Markdown")

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🌐 Website", url="https://pandooverse.x.rarible.com/")],
        [InlineKeyboardButton("🌊 OpenSea", url="https://opensea.io/collection/pandooverse")],
        [InlineKeyboardButton("🪄 Magic Eden", url="https://magiceden.io/u/BambooLabs")],
        [InlineKeyboardButton("🖼 Rarible", url="https://rarible.com/pandoo-verse")],
        [InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/labsbambooo")],
        [InlineKeyboardButton("🐦 Twitter/X", url="https://x.com/GenesisDodo")],
        [InlineKeyboardButton("📘 Facebook", url="https://www.facebook.com")],  # Replace with your actual FB URL
    ]
    await update.message.reply_text("🔗 Explore the *Pandoo-Verse* ecosystem:", reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")

async def nft_metadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/nft <token_id>`", parse_mode="Markdown")
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
        await update.message.reply_text("⚠️ Usage: `/price <slug>`", parse_mode="Markdown")
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
    await update.message.reply_text(f"💰 Floor Price: {floor}\n💵 Volume: {volume}", parse_mode="Markdown")

async def random_nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    url = f"https://api.opensea.io/api/v2/chain/polygon/contract/{CONTRACT_ADDRESS}/nfts?limit=20"
    headers = {"X-API-KEY": API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                await query.message.reply_text("❌ Couldn't fetch NFTs.")
                return
            data = await resp.json()

    nfts = data.get("nfts", [])
    if not nfts:
        await query.message.reply_text("⚠️ No NFTs found.")
        return

    nft = random.choice(nfts)
    name = nft.get("name", "Unnamed")
    image = nft.get("image_url", "")
    token_id = nft.get("identifier")
    traits = nft.get("traits", [])

    # Get mood trait
    mood = "Unknown"
    for trait in traits:
        if trait["trait_type"].lower() == "mood":
            mood = trait["value"]
            break

    caption = f"🎨 *{name}*\n😊 *Mood:* {mood}\n\n🛒 Buy this NFT:"
    buttons = [
        [InlineKeyboardButton("🌊 OpenSea", url=f"https://opensea.io/assets/matic/{CONTRACT_ADDRESS}/{token_id}")],
        [InlineKeyboardButton("🖼 Rarible", url=f"https://rarible.com/token/polygon/{CONTRACT_ADDRESS}:{token_id}")],
        [InlineKeyboardButton("🪄 Magic Eden", url="https://magiceden.io/u/BambooLabs")]
    ]

    await query.message.reply_photo(photo=image, caption=caption, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")

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
    logging.info("Polling started...")
    await app.run_polling()

# Replit-safe asyncio
if __name__ == "__main__":
    import nest_asyncio
    import asyncio

    nest_asyncio.apply()  # Allows nested event loops (fix for Replit)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
