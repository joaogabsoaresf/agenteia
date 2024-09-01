import os
from dotenv import load_dotenv
from api_handler import ApiHandler
load_dotenv()


class ZApi:
    def __init__(self) -> None:
        self.ZAPI_CLIENT_TOKEN = os.getenv('ZAPI_CLIENT_TOKEN')
        self.ZAPI_INSTANCE = os.getenv('ZAPI_INSTANCE')
        self.ZAPI_INSTANCE_TOKEN = os.getenv('ZAPI_INSTANCE_TOKEN')
        self.BASE_URL = f'https://api.z-api.io/instances/{self.ZAPI_INSTANCE}/token/{self.ZAPI_INSTANCE_TOKEN}'
    
    def headers(self):
        return {'Client-Token':self.ZAPI_CLIENT_TOKEN}

class ZApiReceiver(ZApi):
    def __init__(self, data) -> None:
        super().__init__()
        self.data = data
        self.from_me = data.get('fromMe', False)
        self.sender = data.get('senderName', None)
        self.phone = data.get('phone')
        self.text = data.get('text', {}).get('message')
        
class ZApiSender(ZApi):
    def __init__(self, data) -> None:
        super().__init__()
        self.phone = data['phone']
        self.message = data['message']
        # self.message_id = data['messageId']
        
    def send_message(self):
        url = f'{self.BASE_URL}/send-text'
        body = {'phone':self.phone, 'message':self.message}
        return ApiHandler.post(url, self.headers(), body)
        
        
    