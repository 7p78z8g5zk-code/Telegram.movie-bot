import os
import asyncio
import aiohttp
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv('config.env')

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(name)

async def handle_movie_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle text messages containing movie/anime names
    Works in groups and channels
    """
    # Get message text (movie/anime name)
    movie_name = update.message.text.strip()
    
    if not movie_name:
        return
    
    try:
        # Send request to PHP API
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}?query={movie_name}") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('status') == 'found':
                        # Movie found - reply with link
                        await update.message.reply_text(data['link'])
                    else:
                        # Movie not found
                        await update.message.reply_text("❌ Better luck next time 😔")
                else:
                    logger.error(f"API error: {response.status}")
                    await update.message.reply_text("❌ Better luck next time 😔")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text("❌ Better luck next time 😔")

def main():
    """Start the bot"""
    if not BOT_TOKEN or not API_URL:
        logger.error("BOT_TOKEN or API_URL not found in config.env")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handler for text messages (works in groups/channels)
    # IMPORTANT: Bot privacy must be DISABLED in @BotFather for group messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie_message))
    
    # Start bot
    logger.info("Starting Movie Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if name == 'main':
    main()
