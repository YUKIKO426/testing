#!/bin/bash

# Install required dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the bot
echo "Starting the Telegram bot..."
python bot.py
