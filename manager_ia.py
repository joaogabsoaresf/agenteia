import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('OPENAI')
    
class ManagerIA:
    def __init__(self, data) -> None:
        self.client = OpenAI(api_key=api_key)
        self.MANAGER_AGENT_ID = 'asst_J6Uq1bhlq9UvX529rrPsRabV'
        self.data = data
        self.thread = None
        
    def create_thread(self):
        thread = self.client.beta.threads.create()
        self.thread = thread
        
    def create_message(self):
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role='user',
            content=self.data.get('content')
        )
    
    def run(self):
        self.create_thread()
        self.create_message()
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.MANAGER_AGENT_ID,
        )
        while run.status in ['queued', 'in_progress', 'cancelling']:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )
        if run.status == 'completed':
            response = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            return response
        else:
            print('Erro', run.status)
            
    @classmethod
    def extract_messages(cls, response):
        for message in response:
            for msg in message.content:
                return msg.text.value
        
    def get_response(self):
        response = self.run()
        message = self.extract_messages(response)
        if not message:
            return 'Não consegui entender sua questão...'
        return message

