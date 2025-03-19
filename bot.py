import smtplib
import logging
import asyncio
import threading
from fastapi import FastAPI, BackgroundTasks, Form
from email.message import EmailMessage
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7200863338:AAHB5vASJK7luUk9K2OIa1suB2b-Jf4BsIQ"

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"  # Change this if using a different provider
SMTP_PORT = 465
SMTP_EMAIL = "asssasin105@gmail.com"
SMTP_PASSWORD = "pnyx uzyx cnhu endu"

# FastAPI App
app = FastAPI()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("Logger initialized successfully!")

# Telegram Bot Handlers
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a message with emails and content to send mass emails.")

async def send_email(update: Update, context: CallbackContext):
    message_text = update.message.text
    lines = message_text.split("\n")
    
    if len(lines) < 2:
        await update.message.reply_text("Please provide emails and message content properly.")
        return

    emails = lines[0].split(",")  # First line is email list
    email_content = "\n".join(lines[1:])  # Remaining lines are the message

    for email in emails:
        send_mass_email(email.strip(), "Mass Email from Telegram Bot", email_content)
    
    await update.message.reply_text("Emails sent successfully!")

def send_mass_email(to_email: str, subject: str, body: str):
    try:
        msg = EmailMessage()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent to {to_email}")

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")

# Telegram Bot Setup
telegram_bot = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
telegram_bot.add_handler(CommandHandler("start", start))
telegram_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_email))

@app.post("/send-email/")
async def send_email_api(background_tasks: BackgroundTasks, emails: str = Form(...), subject: str = Form(...), message: str = Form(...)):
    email_list = emails.split(",")
    for email in email_list:
        background_tasks.add_task(send_mass_email, email.strip(), subject, message)
    
    return {"message": "Emails are being sent in the background"}

if __name__ == "__main__":
    import uvicorn
    from threading import Thread

    # Run Telegram bot in a separate thread
async def run_telegram_bot():
    print("Running Telegram Bot...")
    await asyncio.sleep(3600)  # Run for an hour as an example

if __name__ == "__main__":
    asyncio.run(run_telegram_bot())
    # Start FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)
