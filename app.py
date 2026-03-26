from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, render_template, request
import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import config and takeover
from config import BOT_TOKEN, ADMIN_USER_ID, TARGET_GROUP_ID
from takeover import full_takeover

app = Flask(__name__)

# ====================== Telegram Bot ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ Unauthorized")
        return
    await update.message.reply_text("""
🤖 Spector Bot Active!

Commands:
/hack @username   - Attempt takeover
    """)

async def hack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        return
    if not context.args:
        await update.message.reply_text("Usage: /hack @username")
        return

    username = context.args[0].replace('@', '')
    await update.message.reply_text(f"🔄 Trying on @{username}...")

    try:
        result = await full_takeover(BOT_TOKEN, username, TARGET_GROUP_ID)
        status = "✅" if result.get("status") == "success" else "❌"
        await update.message.reply_text(f"{status} {result.get('message', str(result))}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# ====================== Flask (Optional) ======================
@app.route('/')
def dashboard():
    return render_template('index.html')

# ====================== Main ======================
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hack", hack_command))

    print("🤖 Bot starting... Press Ctrl+C to stop")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()