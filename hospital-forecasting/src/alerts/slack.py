import requests
import os

def send_slack_alert():
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

    if not webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL is not set in environment variables")

    payload = {
        "text": ":warning: *Forecast model underperforming!* MAE exceeded threshold."
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned error {response.status_code}, {response.text}")
