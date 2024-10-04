from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text=f"Привет! Какss я могу помочь? Твой ID: {user_id}")

def main():
    bot_token = '7330108104:AAGR35aQZ7b-1kHZxIYb-6fB3wICgOQmf00'
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == '__main__':
    main()