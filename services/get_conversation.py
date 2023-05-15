import requests
import sys

def get_conversation(channel_id : str, access_token : str):
    URL = "https://slack.com/api/conversations.history"
    headers = {"Authorization" : "Bearer "+access_token}
    response = requests.post(URL, json = { "channel" : channel_id, "limit" : 7}, headers = headers)
    js = response.json()
    conversation_history = []
    lst = js["messages"][::-1]
    for i in lst:
        if i.get('bot_id', False):
            conversation_history.append({'role' : 'assistant', 'content' : i['text']})
        else:
            text = i['text']
            if '>' in text:
                text = text[text.index('>') + 1 :]
            conversation_history.append({'role' : 'user', 'content' : text})
    #print(conversation_history)
    return conversation_history
