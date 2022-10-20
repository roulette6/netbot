import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from netbot import NetBot

# Initialize a Flask app to host the events adapter
app = Flask(__name__)

# Create an events adapter and register it to an endpoint
# in the slack app for event ingestion
slack_events_adapter = SlackEventAdapter(
    os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app
)

# Initialize a web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))


def get_help(channel):
    """
    Craft the NetBot and send help text to the channel
    """

    # Create a new NetBot
    netbot = NetBot(channel)

    # Get the help message payload
    message = netbot.send_help_info()

    # Post the help message in Slack
    slack_web_client.chat_postMessage(**message)


# When the events adapter detects a message, forward that
# payload to this function
@slack_events_adapter.on("message")
def message(payload):
    """
    Parse the message event, and call a function based
    on the command.
    """

    # Get the event data from the payload
    event = payload.get("event", {})

    # Get the text from the event that came through
    text = event.get("text")

    # Check if the help phrase was in the text of the
    # message. If so, execute the code to flip a coin.
    if "netbot help" in text.lower():
        # Since the activation phrase was met, get the
        # channel ID the event was executed on
        channel_id = event.get("channel")

        # Execute the flip_coin function and send result
        # to the channel
        return get_help(channel_id)


if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase
    # verbosity of log messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run your app on your externally facing IP addr
    # on port 3000 instead of loopback
    app.run(host="0.0.0.0", port=3000)