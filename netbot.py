import json
import os
import urllib3
from napalm import get_network_driver
from yaml import safe_load


class NetBot:
    """
    Define NetBot class to interact with network devices
    based on messages sent by Slack users
    """

    USERNAME = os.environ.get("NTWK_USER")
    PASSWORD = os.environ.get("NTWK_PASSWD")
    HELP_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            # "text": ("Here are the things you can ask me to do:\n")
            "text": (
                "Here are the things you can ask me to do:\n\n"
                "```\n"
                "# get interface information\n"
                "netbot get interface info device=<device name>\n\n"
                "# get routes\n"
                "netbot get routes device=<device name>\n\n"
                "# get HSRP brief output\n"
                "netbot get hrsp device=<device name>\n"
                "```"
            ),
        },
    }

    def __init__(self, channel, device_name=""):
        """
        Class constructor
        """
        self.channel = channel
        self.device_name = device_name

    def send_help_info(self):
        """
        Send help info to users know what to do
        """

        return {
            "channel": self.channel,
            "blocks": [self.HELP_BLOCK],
        }
