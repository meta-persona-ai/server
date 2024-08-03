import datetime
import requests
import pytz
import os

webhook_url = os.getenv('WEBHOOK_URL')
send_webhook_message = os.getenv('SEND_WEBHOOK_MESSAGE')

# Send message to Discord channel
def discord_send_embed_message(title, description, color=0x3498db, username="Server Admin"):
    if not webhook_url:
        return
    if send_webhook_message == "false":
        return
    
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_local = now_utc.astimezone(pytz.timezone('Asia/Seoul'))
    timestamp = now_local.isoformat()  # Convert to ISO 8601 format

    message = {
        "username": username,
        "embeds": [
            {
                "author": {
                    "name": "eMoGi",
                    "url": "",
                    "icon_url": "https://emogi.s3.ap-northeast-2.amazonaws.com/e475b23e-7bfd-4ca3-8d37-770923cb57c8.png"
                },
                "title": title,
                "description": description,
                "timestamp": timestamp,
                "color": color
            }
        ]
    }
    response = requests.post(webhook_url, json=message)
    if response.status_code != 204:
        print(f"Failed to send message to Discord: {response.status_code}, {response.text}")

# Send server start message
def server_start_message():
    title = "Server Start"
    description = "The emogi server has successfully started."
    discord_send_embed_message(title, description, 0x32CD32)  # Green

# Send server stop message
def server_stop_message():
    title = "Server Stop"
    description = "The emogi server has successfully stopped."
    discord_send_embed_message(title, description, 0xCD5C5C)  # Red

# Send environment variable loading failure message
def env_loading_failure_message(component_list: list):
    title = "❌ Environment Variable Loading Failure"
    message = ''.join([f"\n{component}" for component in component_list])
    description = f"Error loading settings: {message}"

    discord_send_embed_message(title, description, 0xffa500)  # Orange

def validate_api_key_failure_message():
    title = "❌ API Key Validation Failure"
    description = f"Google API key validation failed:"
    discord_send_embed_message(title, description, 0xffa500)  # Orange