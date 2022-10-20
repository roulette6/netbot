from slack import WebClient
from coinbot import CoinBot
import os

# Crate a slack client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

# Get a new coinbot
bot = CoinBot("#networking-chatbox")

# Get the onboarding message payload
message = bot.get_message_payload()

# Post the onboarding message payload
slack_web_client.chat_postMessage(**message)
