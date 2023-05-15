import pickle

def print_db():
    with open('db.pickle','rb+') as handle:
        b = pickle.load(handle)
        print(b)

def get_access_token(team_id : str):
    with open('db.pickle', 'rb+') as handle:
        b = pickle.load(handle)
        #return b.get(team_id, None)
        return b[team_id]['access_token']
def dump_into_db(json_data):
    with open('db.pickle', 'rb+') as handle:
        b = pickle.load(handle)    
    #{'ok': True, 'app_id': 'A053KC0656F', 'authed_user': {'id': 'U053CSUM8H4'}, 'scope': 'app_mentions:read,channels:history,channels:read,chat:write.public,chat:write,channels:join,im:history,im:write,im:read,mpim:history,mpim:read,mpim:write,commands', 'token_type': 'bot', 'access_token': 'xoxb-5145206166352-5121431182243-1LFlKQ3gw8KW9NEaL4F7OzME', 'bot_user_id': 'U053KCP5C75', 'team': {'id': 'T0549624WAC', 'name': 'demo-01'}, 'enterprise': None, 'is_enterprise_install': False}
    b[json_data['team']['id']] = {"team_name" : json_data['team']['name'], "access_token" : json_data['access_token']}
    with open('db.pickle', 'wb+') as handle:
        pickle.dump(b, handle)