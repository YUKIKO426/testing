import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Email configuration
SMTP_SERVER = 'https://smtp.gmail.com'  # Replace with your SMTP server
SMTP_PORT = 465  # For SSL, use 465; for TLS, use 587
SMTP_USERNAME = 'asssasin105@gmail.com'
SMTP_PASSWORD = 'pnyx uzyx cnhu endu'

# List of recipient emails
RECIPIENTS = ['mail@bka.bund.de', 'dsa.telegram@edsr.eu']

# Function to send emails
def send_mass_email(subject: str, body: str) -> None:
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            for recipient in RECIPIENTS:
                msg['To'] = recipient
                server.sendmail(SMTP_USERNAME, recipient, msg.as_string())
        print('Emails sent successfully.')
    except Exception as e:
        print(f'Failed to send emails: {e}')

# Telegram command handler
async def send_email_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text('Usage: /sendemail <subject> <body>')
        return

    subject = context.args[0]
    body = ' '.join(context.args[1:])
    send_mass_email(subject, body)
    await update.message.reply_text('Emails have been sent.')

def main() -> None:
    # Initialize the Telegram bot
    application = Application.builder().token('7200863338:AAHB5vASJK7luUk9K2OIa1suB2b-Jf4BsIQ').build()

    # Register the command handler
    application.add_handler(CommandHandler('sendemail', send_email_command))

    # Start the bot
    application.run_polling()

if name == 'main':
    main()
