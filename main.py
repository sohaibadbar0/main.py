from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update\
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler\
import random\
\
BOT_TOKEN = "7783908047:AAFoeBzu7qQGLHFmiehu3HswF0rJtZD2I08"\
\
# \uc0\u9989  Sample NFT images \
NFT_IMAGES = [\
    "https://ipfs.raribleuserdata.com/ipfs/bafybeica5pnqglknw52frn36tfdvydnp7llpohz7x5lqmpys2ll3fhtk34/image.png",\
    "https://ipfs.raribleuserdata.com/ipfs/bafybeigbhbmuzhejjxiy3267j3fcgf33vxjoubwp6ipkdzwhmrxj6jpbsi/image.png",\
    "https://ipfs.raribleuserdata.com/ipfs/bafybeiacu4agkutieq7x6aaf7zr5fafqac5fyowjayzsgyyhy2r6vnzlda/image.png"\
]\
\
# \uc0\u55356 \u57262  /start Command\
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    keyboard = [\
        [InlineKeyboardButton("\uc0\u55356 \u57262  Launch Mini Game", url="https://t.me/Pandooverse_bot/Pandooverse")],\
        [InlineKeyboardButton("\uc0\u55357 \u56764  Show Random NFT", callback_data='random_nft')],\
        [InlineKeyboardButton("\uc0\u55356 \u57104  Explore Collections", callback_data='show_links')]\
    ]\
    reply_markup = InlineKeyboardMarkup(keyboard)\
    await update.message.reply_text("\uc0\u55357 \u56395  Welcome to the PANDOO-VERSE Bot!", reply_markup=reply_markup)\
\
# \uc0\u55357 \u56550  NFT data with metadata + links\
NFTS = [\
    \{\
        "name": "ZOMBOO",\
"mood": "UNDEAD-VENGEANCE",\
        "image": "https://ipfs.raribleuserdata.com/ipfs/bafybeigbhbmuzhejjxiy3267j3fcgf33vxjoubwp6ipkdzwhmrxj6jpbsi/image.png",\
        "links": \{\
            "OpenSea": "https://opensea.io/item/matic/0x25b9076dcd51f64ae556a40e3416fd1d4aabb730/93796537342832024675967128742781221386530876313527858511457224352888159993880",\
            "Magic Eden": "
\fs32 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 https://magiceden.io/u/BambooLabs?chains=%5B%22polygon%22%5D&wallets=%5B%220xcF5eF574408CdEa126DD4Acc24067892c7D6C2F0%22%5D
\fs24 \cf0 \cb1 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 ",\
            "Rarible": "https://rarible.com/token/polygon/0x25b9076dcd51f64ae556a40e3416fd1d4aabb730:93796537342832024675967128742781221386530876313527858511457224352888159993880",\
            "Official Site": "https://pandooverse.x.rarible.com/token/POLYGON:0x25b9076dcd51f64ae556a40e3416fd1d4aabb730:93796537342832024675967128742781221386530876313527858511457224352888159993880"\
        \}\
    \},\
    \{\
        \
 "name": "PLAYER 456",\
        "mood": "REVENGE SEEKING",\
        "image": "https://ipfs.raribleuserdata.com/ipfs/bafybeica5pnqglknw52frn36tfdvydnp7llpohz7x5lqmpys2ll3fhtk34/image.png",\
        "links": \{\
            "OpenSea": "https://opensea.io/item/matic/0x25b9076dcd51f64ae556a40e3416fd1d4aabb730/93796537342832024675967128742781221386530876313527858511457224352888159993865",\
            "Magic Eden": "https://magiceden.io/u/BambooLabs?chains=%5B%22polygon%22%5D&wallets=%5B%220xcF5eF574408CdEa126DD4Acc24067892c7D6C2F0%22%5D",\
            "Rarible": "https://rarible.com/token/polygon/0x25b9076dcd51f64ae556a40e3416fd1d4aabb730:93796537342832024675967128742781221386530876313527858511457224352888159993865",\
            "Official Site": "https://pandooverse.x.rarible.com/token/POLYGON:0x25b9076dcd51f64ae556a40e3416fd1d4aabb730:93796537342832024675967128742781221386530876313527858511457224352888159993865"\
        \}\
    \},\
    # Add more NFTs here...\
]\
\
# \uc0\u55357 \u56764  Show Random NFT with details + links\
async def random_nft(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    query = update.callback_query\
    await query.answer()\
    \
    nft = random.choice(NFTS)\
    links = "\\n".join([f"- [\{k\}](\{v\})" for k, v in nft["links"].items()])\
\
    caption = (\
        f"\uc0\u55356 \u57225  Here's a random drop from the *PANDOO-VERSE!*\\n\\n"\
        f"\uc0\u55358 \u56824  *\{nft['name']\}*\\n"\
        f"\uc0\u55358 \u56800  *Mood:* \{nft['mood']\}\\n\\n"\
        f"\uc0\u55357 \u56599  *Buy on:*\\n\{links\}"\
    )\
\
    await query.message.reply_photo(\
        photo=nft["image"],\
        caption=caption,\
        parse_mode="Markdown"\
    )\
\
# \uc0\u55356 \u57104  Show Collection Links\
async def show_links(update: Update, context: ContextTypes.DEFAULT_TYPE):\
    query = update.callback_query\
    await query.answer()\
    links_text = (\
        "\uc0\u55357 \u57042  Explore the PANDOO-VERSE Collections:\\n"\
        "- [OpenSea](https://opensea.io/collection/pandooverse)\\n"\
        "- [Magic Eden](https://magiceden.io/u/BambooLabs?chains=%5B%22polygon%22%5D)\\n"\
        "- [Rarible](https://pandooverse.x.rarible.com/)\\n"\
        "- [Official Site](https://pandooverse.x.rarible.com/)"\
    )\
    await query.message.reply_text(links_text, parse_mode='Markdown')\
\
# Run the bot\
def main():\
    app = ApplicationBuilder().token(BOT_TOKEN).build()\
    app.add_handler(CommandHandler("start", start))\
    app.add_handler(CallbackQueryHandler(random_nft, pattern="random_nft"))\
    app.add_handler(CallbackQueryHandler(show_links, pattern="show_links"))\
    print("\uc0\u55358 \u56598  Bot is running...")\
    app.run_polling()\
\
if __name__ == "__main__":\
    main()}
