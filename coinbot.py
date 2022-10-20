import random


class CoinBot:
    # Create a constant that contains the default
    # message text
    COIN_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ("Flipping a coin:\n\n"),
        },
    }

    # Constructor takes the channel name as the parameter
    # and sets it as an instance var
    def __init__(self, channel):
        self.channel = channel

    # Generate a random number to simulate flipping a coin.
    # Return the crafted slack payload with the coin flip message
    def _flip_coin(self):
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            result = "Heads"
        else:
            result = "Tails"

        text = f"The result is `{result}`"

        return ({"type": "section", "text": {"type": "mrkdwn", "text": text}},)

    # Craft and return the entire message payload as a dict
    def get_message_payload(self):
        return {
            "channel": self.channel,
            "blocks": [
                self.COIN_BLOCK,
                *self._flip_coin(),
            ],
        }
