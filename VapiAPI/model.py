from config import PHONE_NUMBER_ID,assistant_id
from utils import get_prompt_from_file
class CallData:
    def __init__(self, customer_number: str, 
                 first_message: str = "Hey, what's up?",
                 provider: str = "openai",
                 model: str = "gpt-3.5-turbo",
                 content: str = "You are an assistant.",
                 voice: str = "jennifer-playht"):
        
        self.data = {
            'assistant': {
                "firstMessage": first_message,
                "model": {
                    "provider": provider,
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": content
                        }
                    ]
                },
                "voice": voice
            },
            'phoneNumberId': PHONE_NUMBER_ID,
            'customer': {
                'number': customer_number,
            },
        }

    def get_data(self) -> dict:
        return self.data


class Persona:
    def __init__(self,phoneNumber,linkedinUrl,websiteUrl):
        self.data = {
            "phoneNumber": phoneNumber,
            "linkedinUrl": linkedinUrl,
            "websiteUrl": websiteUrl
        }

class preData:
    def __init__(self,customer_number,sales_person_name,company_name,product_summary):
        self.assistant_id =assistant_id
        self.phone_number_id = PHONE_NUMBER_ID
        self.customer_number = customer_number
        self.first_message = get_prompt_from_file(prompt_name="first_msg.txt").format(sales_person_name=sales_person_name,company_name=company_name)
        self.prompt =get_prompt_from_file(prompt_name="main_prompt.txt").format(product_summary=product_summary,sales_person_name=sales_person_name,company_name=company_name)
        self.data = {
            'assistantId': self.assistant_id,
            'assistant': {
                'firstMessage': self.first_message,
                'model':{
                    'provider': 'openai',
                    # 'url':'https://api.openai.com/v1/chat/completions',
                    'model':'gpt-4o',
                    "messages": [
                        {
                            "role": "system",
                            "content": self.prompt
                        }
                    ]
                }
            },
            'phoneNumberId': self.phone_number_id,
            'customer': {
                'number': self.customer_number
            }
        }
    def get_data(self):
        return self.data



class CallStatusData:
    def __init__(self, response_json):
        self.call_id = response_json.get("id")
        self.assistant_id = response_json.get("assistantId")
        self.type = response_json.get("type")
        self.status = response_json.get("status")
        self.started_at = response_json.get("startedAt")
        self.ended_at = response_json.get("endedAt")
        self.transcript = response_json.get("transcript")
        self.recording_url = response_json.get("recordingUrl")
        self.summary = response_json.get("summary")
        self.phone_call_provider = response_json.get("phoneCallProvider")
        self.ended_reason = response_json.get("endedReason")
        self.created_at = response_json.get("createdAt")
        self.updated_at = response_json.get("updatedAt")
        self.messages = response_json.get("messages")

    def to_dict(self):
        return {
            "call_id": self.call_id,
            "assistant_id": self.assistant_id,
            "type": self.type,
            "status": self.status,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "transcript": self.transcript,
            "recording_url": self.recording_url,
            "summary": self.summary,
            "phone_call_provider": self.phone_call_provider,
            "ended_reason": self.ended_reason,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "messages": self.messages,
        }
