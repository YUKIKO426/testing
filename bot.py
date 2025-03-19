import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Replace these with your email and password
EMAIL_ADDRESS = 'asssasin105@gmail.com'
EMAIL_PASSWORD = 'pnyx uzyx cnhu endu'

# Create a function to send emails
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

# Command handler for /sendmassmail
def start(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 3:
        update.message.reply_text("Hello! I am your bot.")
        return

    subject = context.args[0]
    body = ' '.join(context.args[1:-1])
    recipients = context.args[-1].split(',')

    success_count = 0
    for recipient in recipients:
        recipient = recipient.strip()
        if send_email(recipient, subject, body):
            success_count += 1

    update.message.reply_text(f"Sent emails to {success_count}/{len(recipients)} recipients.")

def main():
    app = Application.builder().token("7200863338:AAHB5vASJK7luUk9K2OIa1suB2b-Jf4BsIQ").build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()  # Make sure this line is properly indented

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
