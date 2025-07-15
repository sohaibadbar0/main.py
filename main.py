import os
import logging
import random
import aiohttp
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
CONTRACT_ADDRESS = "0x25b9076dcd51f64ae556a40e3416fd1d4aabb730"

# Logging
logging.basicConfig(level=logging.INFO)

# Sample images for demo
NFT_IMAGES = [
    "https://ipfs.raribleuserdata.com/ipfs/bafybeica5pnqglknw52frn36tfdvydnp7llpohz7x5lqmpys2ll3fhtk34/image.png",
    "https://ipfs.raribleuserdata.com/ipfs/bafybeigbhbmuzhejjxiy3267j3fcgf33vxjoubwp6ipkdzwhmrxj6jpbsi/image.png",
]

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Launch Mini Game", url="https://t.me/Pandooverse_bot/Pandooverse")],
        [InlineKeyboardButton("🖼 Show Random NFT", callback_data='random_nft')],
        [InlineKeyboardButton("🌐 Explore Links", callback_data='show_links')],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎉 Welcome to *PANDOO-VERSE*!", reply_markup=markup, parse_mode="Markdown")

# /help command
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 *Available Commands:*\n"
        "/start - Show menu\n"
        "/nft <token_id> - View metadata\n"
        "/price <collection_slug> - View floor price\n"
        "/about - Project info\n"
        "/links - Marketplace links",
        parse_mode="Markdown"
    )

# /about command
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐼 *PANDOO-VERSE* is a panda-powered NFT universe with battles, traits, and stories.\n"
        "Explore: https://pandooverse.x.rarible.com/",
        parse_mode="Markdown"
    )

# /links command
async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🌐 Website", url="https://pandooverse.x.rarible.com/")],
        [InlineKeyboardButton("📦 OpenSea", url="https://opensea.io/collection/pandooverse")],
        [InlineKeyboardButton("🧙 Magic Eden", url="https://magiceden.io/u/BambooLabs")],
        [InlineKeyboardButton("🖼 Rarible", url="https://rarible.com/pandoo-verse")]
    ]
    await update.message.reply_text("🔗 Explore more:", reply_markup=InlineKeyboardMarkup(buttons))

# /nft <token_id>
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
                await update.message.reply_text("❌ Couldn't fetch metadata. Try again.")
                return
            data = await resp.json()

    nft = data.get("nft", {})
    name = nft.get("name", "Unnamed")
    image = nft.get("image_url", "")
    desc = nft.get("description", "No description.")
    traits = nft.get("traits", [])

    trait_list = "\n".join([f"- *{t['trait_type']}*: {t['value']}" for t in traits]) if traits else "No traits."
    caption = f"🎨 *{name}*\n\n🖼 {desc}\n\n🎯 *Traits:*\n{trait_list}"
    await update.message.reply_photo(photo=image, caption=caption, parse_mode="Markdown")

# /price <collection_slug>
async def floor_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usage: `/price <collection_slug>`", parse_mode="Markdown")
        return
    slug = context.args[0]
    url = f"https://api.opensea.io/api/v2/collections/{slug}/stats"
    headers = {"X-API-KEY": API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                await update.message.reply_text("🚫 API Error. Try again.")
                return
            data = await resp.json()
            stats = data.get("total", {})

    floor = stats.get("floor_price", "N/A")
    volume = stats.get("total_volume", "N/A")
    await update.message.reply_text(
        f"📉 *Floor Price:* {floor}\n📈 *Total Volume:* {volume
