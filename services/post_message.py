import requests
from .data_storage import get_access_token

def post_message(message, channel, team_id):
    URL = "https://slack.com/api/chat.postMessage"
    access_token = get_access_token(team_id)
    headers = {"Authorization" : "Bearer "+access_token}
    response = requests.post(URL, data = {"channel" : channel, "text" : message}, headers = headers)
    if response.status_code == 200:
        return True
    return False
