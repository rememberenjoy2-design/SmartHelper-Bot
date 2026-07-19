import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from duckduckgo_search import DDGS

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Load your Telegram token from Railway environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets the user when they send /start."""
    await update.message.reply_text("Hello! Ask me any question, and I will answer it using free open AI models.")

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Takes the question, asks DuckDuckGo AI, and replies."""
    user_message = update.message.text
    
    # Show that the bot is typing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Use DDGS to chat with a free open-source model (like Llama 3) without an API key
        with DDGS() as ddgs:
            # choices for model: 'gpt-4o-mini', 'meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo', etc.
            response = ddgs.chat(user_message, model='gpt-4o-mini')
            
        await update.message.reply_text(response)
    except Exception as e:
        logging.error(f"Error getting AI response: {e}")
        await update.message.reply_text("Sorry, I had trouble answering that question right now.")

if __name__ == '__main__':
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN variable is missing!")
        exit(1)
        
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    
    logging.info("Starting bot without API keys...")
    app.run_polling()
