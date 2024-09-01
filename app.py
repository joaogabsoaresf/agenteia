import os
import json
from dotenv import load_dotenv
from flask import Flask, request, Response
from manager_ia import ManagerIA
from z_api import ZApiReceiver, ZApiSender
from threading import Thread
from responses import success_response, from_user_response, service_off_response, not_authorized_response, incorrect_chat_response
load_dotenv()

app = Flask(__name__)

Z_API_TOKEN = os.getenv('ZAPI')
GROUP_ID = os.getenv('GROUP_ID')

@app.before_request
def before_request_middleware():
    if request.path == '/manager' and request.method == 'POST':
        if not bool(int(os.getenv('SERVICE_ON'))):
            return service_off_response()
        auth_token = request.headers.get('z-api-token')
        if not auth_token or auth_token != Z_API_TOKEN:
            return not_authorized_response()

@app.route('/')
def index():
    return 'OK'

@app.route('/manager', methods=['POST'])
def manager():
    receiver = ZApiReceiver(request.json)
    if receiver.from_me:
        return from_user_response()
    if not receiver.is_group or receiver.chat_name != 'ManagerIA':
        return incorrect_chat_response()
    if receiver.phone != GROUP_ID:
        return incorrect_chat_response()
    
    def send_response():
        manager_ia_data = {'content':receiver.text}
        manager_ia = ManagerIA(manager_ia_data)
        response_data = {'phone':receiver.phone, 'message':manager_ia.get_response()}
        sender = ZApiSender(response_data)
        sender.send_message()
        
    t = Thread(target=send_response, args=())
    t.start()
        
    return success_response(response='success')

