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
    b[json_data['team']['id']] = {"team_name" : json_data['team']['name'], "access_token" : json_data['access_token']}
    with open('db.pickle', 'wb+') as handle:
        pickle.dump(b, handle)