from fastapi import FastAPI, Request, Response, status
import json
from typing import Optional
import requests
from services.get_conversation import get_conversation
from services.data_storage import *
from services.post_message import post_message
from services.extract_event_info import extract_info
import os  
import time

app = FastAPI()


@app.get('/')
def index():
    return {"status" : "OK"}

@app.get('/bot_auth')
async def bot_auth(code : str, state : str = Optional[None]):
    global CLIENT_ID, CLIENT_SECRET
    response = requests.post("https://slack.com/api/oauth.v2.access", data={"client_id" : CLIENT_ID , "client_secret" : CLIENT_SECRET , "code" : code})
    raw = json.loads(response.content.decode('ascii'))
    dump_into_db(raw)
    return {"Bot Install" : "Successfull"}


@app.post('/receive_events')
async def receive_events(req : Request, ):
    global BEARER_TOKEN
    global LINK
    global U_TIME
    raw = await req.body()
    raw = raw.decode('ascii')
    try:
        raw = json.loads(raw)
        if raw.get("challenge", False):
            return raw["challenge"]
        ts = float(raw['event']['ts'])
        if ts > U_TIME:
            U_TIME = ts
        else:
            print("REPEATED EVENT************")
            return None
        text, channel, team_id = extract_info(raw)
        headers = {"Authorization" : "Bearer "+BEARER_TOKEN}
        conversation = get_conversation(channel, get_access_token(team_id))
        if conversation[-1]['role'] == 'user':
            res = requests.post(LINK, json = {"text" : text, "channel" : channel,"conversation_history" : conversation}, headers=headers)
            print(res.status_code)        
        print("Text:",text,";in channel:",channel)            
        headers = {"Authorization" : "Bearer "+BEARER_TOKEN}
        conversation = get_conversation(channel, get_access_token(team_id))
        print(conversation)
        if conversation[-1]['role'] == 'user':        
            res = requests.post(LINK, json = {"text" : text, "channel" : channel,"conversation_history" : conversation}, headers=headers)
            res = res.json()
            answer = res["chatbot_response"]
            print("Bot response:",answer)            
            print(post_message(answer, channel, team_id))        
    except Exception as E:
        print('error',E)
    
@app.on_event("startup")
def startup():
    global BEARER_TOKEN, LINK, U_TIME, CLIENT_ID, CLIENT_SECRET
    U_TIME = 0
    BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
    LINK = os.environ.get("LINK")
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    assert CLIENT_ID is not None
    assert CLIENT_SECRET is not None
    assert BEARER_TOKEN is not None
    assert LINK is not None