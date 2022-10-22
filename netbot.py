from netmiko import ConnectHandler


class NetBot:
    """
    Define NetBot class to interact with network devices
    based on messages sent by Slack users
    """

    HELP_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Here are the things you can ask me to do:\n\n"
                "```\n"
                "# get interface information\n"
                "netbot get interface info device=<device name>\n\n"
                "# get routes\n"
                "netbot get routes device=<device name>\n\n"
                "# get HSRP brief output\n"
                "netbot get hrsp device=<device name>\n"
                "```\n\n"
                "where devices are `rt1` and `rt2`"
            ),
        },
    }

    def __init__(self, channel, device=""):
        """
        Class constructor
        """
        self.channel = channel
        self.device = device

    def send_help_info(self):
        """
        Send help info to users know what to do
        """

        return {
            "channel": self.channel,
            "blocks": [self.HELP_BLOCK],
        }

    def get_routes(self):
        """
        get route table for device indicated
        """

        # Connect to device and get command output
        with ConnectHandler(**self.device) as connection:
            output = connection.send_command("show ip route | b ^Gate")

        return {
            "channel": self.channel,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"Here are the routes for {self.device['host']}:\n\n"
                            "```\n"
                            f"{output}\n"
                            "```\n"
                        ),
                    },
                }
            ],
        }

    def get_interfaces(self):
        """
        get interface info for device indicated
        """

        # Connect to device and get command output
        with ConnectHandler(**self.device) as connection:
            output = connection.send_command("show ip int brief")

        return {
            "channel": self.channel,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"Here are the interfaces for {self.device['host']}:\n\n"
                            "```\n"
                            f"{output}\n"
                            "```\n"
                        ),
                    },
                }
            ],
        }
