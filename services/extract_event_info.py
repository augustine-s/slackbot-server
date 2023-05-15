

def extract_info(event : dict):
    text = event['event']['text']
    if '>' in text:
        text = text[text.index('>') + 1 : ]
    channel = event['event']['channel']
    team_id = event['team_id']
    return text, channel, team_id