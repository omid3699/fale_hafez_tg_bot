import asyncio
import json
import logging
import os
import random
from uuid import uuid4

from dotenv import load_dotenv
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, CommandHandler, InlineQueryHandler

# Load environment variables
load_dotenv("./.env")
token = os.getenv("Token")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load data from JSON file
with open("./data.json", mode="r") as f:
    data = json.load(f)

# Define command handlers
async def start(update: Update, context) -> None:
    """Send a welcome message when /start is issued."""
    await update.message.reply_text('/fal نیت نموده روی کلیک کنید.')

async def fal(update: Update, context) -> None:
    """Send a random fal."""
    fal_item = random.choice(data)
    await update.message.reply_text(f"{fal_item['ghazal']}\n\n{fal_item['fal']}")

async def inline_fal(update: Update, context) -> None:
    """Handle inline queries to send a random fal."""
    query = update.inline_query.query
    if query == "":
        return

    fal_item = random.choice(data)
    ghazal = fal_item['ghazal']
    fal_text = fal_item['fal']

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Get a fal",
            input_message_content=InputTextMessageContent(f"{ghazal}\n\n{fal_text}")
        )
    ]

    await update.inline_query.answer(results)

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fal", fal))
    application.add_handler(InlineQueryHandler(inline_fal))

    # Start the Bot
    application.run_polling()
    # Run the bot until interrupted
    application.idle()
    

if __name__ == '__main__':

    asyncio.run(main())
