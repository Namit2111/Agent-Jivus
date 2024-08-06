from config import PHONE_NUMBER_ID

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
