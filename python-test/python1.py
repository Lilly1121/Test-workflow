import requests
import os
import sys
from datetime import datetime

# --- CONFIGURATION ---
# Get the Bot Token and Channel Name from environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_NAME = os.getenv("SLACK_CHANNEL_NAME", "#general") # Default to #general if not set

# The Slack API endpoint for posting messages
SLACK_API_URL = "https://slack.com/api/chat.postMessage"

def send_slack_alert_with_token(message, channel):
    """
    Sends a formatted message to a specific Slack channel using a Bot Token.
    """
    if not SLACK_BOT_TOKEN:
        print("Error: SLACK_BOT_TOKEN environment variable not set.")
        return

    # Prepare the headers with the Authorization token
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

    # The payload is similar but now includes the 'channel' key
    payload = {
        "channel": channel,
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 API Token Alert! 🚨",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*When:*\n{current_time}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Location:*\nBengaluru, India"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*:satellite: Message:*\n>{message}"
                }
            }
        ]
    }

    try:
        response = requests.post(SLACK_API_URL, headers=headers, json=payload, timeout=5)
        response_data = response.json()

        # The Slack API response contains an "ok" field
        if response_data.get("ok"):
            print(f"Alert sent successfully to channel '{channel}'!")
        else:
            # Print the error message provided by the Slack API
            error_message = response_data.get("error", "Unknown error")
            print(f"Failed to send alert. Slack API error: {error_message}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the request: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        custom_message = " ".join(sys.argv[1:])
    else:
        custom_message = "API Token test run executed successfully."

    send_slack_alert_with_token(custom_message, SLACK_CHANNEL_NAME)
