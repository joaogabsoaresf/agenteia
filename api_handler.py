import requests
import json
import os
import traceback
from dotenv import load_dotenv
load_dotenv()

class ApiHandler:
    @classmethod
    def post(cls, url, headers, body):
        try:
            response = requests.post(url=url, json=body, headers=headers)
            response.raise_for_status()
        except Exception as e:
            traceback.print_exc(e)
            return
        return response.json()
