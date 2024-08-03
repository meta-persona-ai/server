import datetime
import requests
import pytz

discord_url = "https://discord.com/api/webhooks/1269286718280958025/0ceB8qqw_tnvweSiw8WfvWhmKUWCDVbEVEg5QikUh0Sw5aogu3shk9GF51bRK1DEHReQ"

# Send message to Discord channel
def discord_send_embed_message(title, description, color=0x3498db, username="Server Admin"):
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_local = now_utc.astimezone(pytz.timezone('Asia/Seoul'))
    timestamp = now_local.isoformat()  # Convert to ISO 8601 format
    embed = {
        "title": title,
        "description": description,
        "timestamp": timestamp,
        "color": color
    }
    message = {
        "username": username,
        "embeds": [embed]
    }
    response = requests.post(discord_url, json=message)
    print(message)
    print(response.status_code, response.content)

# Send server start message
def server_start_message():
    title = "Server Start"
    description = "The emogi server has successfully started."
    discord_send_embed_message(title, description, 0x00ff00)  # Green

# Send server stop message
def server_stop_message():
    title = "Server Stop"
    now_local = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    description = f"The emogi server has successfully stopped.\nCurrent time: {now_local.strftime('%Y-%m-%d %H:%M:%S')}"
    discord_send_embed_message(title, description, 0xff0000)  # Red

# Test sending messages
server_start_message()
server_stop_message()
