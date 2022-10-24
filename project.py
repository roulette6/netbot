import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from yaml import safe_load
from netbot import NetBot


# Initialize slack app with bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# listen for debug request
@app.message("netbot debug")
def message_help(message, say):
    debug_msg = ""
    for key, value in message.items():
        debug_msg = debug_msg + f"{key}: {value}\n"
    say(f"```\n{debug_msg}\n```")


# Listen to incoming messages that contain "netbot help"
@app.message("netbot help")
def message_help(message, say):
    """
    Instantiate NetBot and send help text to the channel
    """

    # Create a new NetBot
    netbot = NetBot()

    # Return the help message text
    help_text = netbot.send_help_info()
    say(help_text)


# listen for message requesting routes
@app.message("netbot get")
def send_routes(message, say):
    """
    Instantiate NetBot and get device routes
    """

    # get command device dict from input
    command, device = get_command_and_device(message["text"])

    netbot = NetBot(command, device)

    # Get device routes
    device_routes = netbot.get_output()

    # Post routes in Slack
    say(f"```\n{device_routes}\n```")


def get_command_and_device(message):
    """
    Returns device name given a Slack message
    """

    try:
        # split input into command and device
        command, device_key = message.strip().split(" device=")
    except ValueError:
        # No device found
        return None, None
    else:
        device = get_device_dict(device_key)
        return command, device


def get_device_dict(device=""):
    """
    Accepts a hostname and returns its dict of attr
    """
    # Read hosts file into structured data
    with open("hosts.yml", encoding="utf-8") as file:
        hosts = safe_load(file)

    # Add credentials from env vars
    for host in hosts["host_list"]:
        host["username"] = os.environ.get("NTWK_USERNAME")
        host["password"] = os.environ.get("NTWK_PASSWORD")
    rt1, rt2 = hosts["host_list"]

    devices = {"rt1": rt1, "rt2": rt2}

    try:
        return devices[device]
    except KeyError:
        return None


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
