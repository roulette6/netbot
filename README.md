# NetBot
NetBot is my final project for CS50 Python. It uses [Slack Bolt](https://slack.dev/bolt-python/tutorial/getting-started) to create a socket that listens for Slack events to execute commands on network devices. The link above goes through all steps necessary on the Slack website and Python.

## Requirements
* Slack application (bot) with appropriate permissions as per link above.
* Setting the following environment variables:
    * `NTWK_USERNAME="..."`
    * `NTWK_PASSWORD="..."`
    * `SLACK_APP_TOKEN="xapp..."`
    * `SLACK_BOT_TOKEN="xoxb..."`
* I am using [eve-ng](https://www.eve-ng.net/) to run virtual routers that receive the commands. You can adapt the program to instead run commands on Linux VMs in your own network or a cloud provider.