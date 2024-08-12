from config import PHONE_NUMBER_ID,assistant_id

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
    def __init__(self,customer_number):
        self.assistant_id =assistant_id
        self.phone_number_id = PHONE_NUMBER_ID
        self.customer_number = customer_number
        self.data = {
            'assistantId': self.assistant_id,
            'phoneNumberId': self.phone_number_id,
            'customer': {
                'number': self.customer_number
            }
        }
    def get_data(self):
        return self.data