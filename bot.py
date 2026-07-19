import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Load environment variables from Railway
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize Gemini Client
ai_client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets the user when they send /start."""
    await update.message.reply_text("Hello! Ask me any question, and I will do my best to answer it.")

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Takes any incoming text message, asks Gemini, and replies with the answer."""
    user_message = update.message.text
    
    # Send a typing indicator so the user knows the bot is working
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Generate the response using Gemini 2.5 Flash (fast & smart)
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error generating AI response: {e}")
        await update.message.reply_text("Sorry, I encountered an error trying to process that question.")

if __name__ == '__main__':
    # Build the Telegram application
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    
    # Start the bot using Long Polling (perfect for Railway background services)
    logging.info("Starting bot...")
    app.run_polling()
