import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from yaml import safe_load
from netbot import NetBot

# Initialize a Flask app to host the events adapter
main = Flask(__name__)

# Create an events adapter and register it to an endpoint
# in the slack app for event ingestion
slack_events_adapter = SlackEventAdapter(
    os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", main
)

# Initialize a web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

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

    # Get the text and channel from the event received
    text = event.get("text").lower()
    channel_id = event.get("channel")

    try:
        command, host = text.split(" device=")
    except ValueError:
        command = text
        host = None

    if host:
        # Get dict of device info needed for login
        device = get_device(host)

        # Determine which method to call based on command
        match command:
            case "netbot get routes":
                return get_routes(channel_id, device)
            case "netbot get interface info":
                return get_interfaces(channel_id, device)
    else:
        if command == "netbot help":
            return get_help(channel_id)


def get_help(channel):
    """
    Instantiate NetBot and send help text to the channel
    """

    # Create a new NetBot
    netbot = NetBot(channel)

    # Get the help message payload
    message = netbot.send_help_info()

    # Post the help message in Slack
    slack_web_client.chat_postMessage(**message)


def get_routes(channel, device):
    """
    Instantiate NetBot and get device routes
    """

    # Create a new NetBot
    netbot = NetBot(channel, device)

    # Get device routes
    message = netbot.get_routes()

    # Post routes in Slack
    slack_web_client.chat_postMessage(**message)


def get_interfaces(channel, device):
    """
    Instantiate NetBot and get device routes
    """

    # Create a new NetBot
    netbot = NetBot(channel, device)

    # Get device interfaces
    message = netbot.get_interfaces()

    # Post interfaces in Slack
    slack_web_client.chat_postMessage(**message)


def get_device(device=""):
    # Read hosts file into structured data
    with open("hosts.yml", encoding="utf-8") as file:
        hosts = safe_load(file)

    # Add credentials from env vars
    for host in hosts["host_list"]:
        host["username"] = os.environ.get("NTWK_USERNAME")
        host["password"] = os.environ.get("NTWK_PASSWORD")
    rt1, rt2 = hosts["host_list"]

    devices = {"rt1": rt1, "rt2": rt2}
    return devices[device] if device else ""


if __name__ == "__main__":
    # Create the logging object, increase its verbosity
    # to DEBUG, and add the streamhandler as the
    # logging handler
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    # Run your app on all IP addr instead of only loopback
    main.run(host="0.0.0.0", port=3000)
