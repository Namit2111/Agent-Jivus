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
    def __init__(self,customer_number,sales_person_name,company_name,product_summary):
        self.assistant_id =assistant_id
        self.phone_number_id = PHONE_NUMBER_ID
        self.customer_number = customer_number
        self.first_message = f"Hello, This is {sales_person_name} from {company_name}"
        self.prompt =f"""   
        You are a voice assistant for {company_name}, {product_summary}

Your job is to initiate B2B sales calls and determine if you are speaking with a gatekeeper or the decision-maker. Follow these steps to navigate the conversation:

Introduction and Role Identification:

Start with a polite and professional greeting.
Ask if the person you’re speaking with is responsible for the specific area relevant to your product.
Example: " Hello, This is {sales_person_name} from {company_name} .Can you help me out if I am talking to write person about buying our product,{product_summary}?"
Handling Gatekeepers:

If the person is a gatekeeper, politely ask for information about the decision-maker. Remember the decision makers name which you can use to setup the meeting later
Explain the value of your product and why it’s worth the decision-maker’s time.
Suggest a specific time for a meeting or call with the decision-maker.
Example: "I understand you might not be the person handling this directly, but could you help me connect with [Decision Maker’s Name] as we have a solution that could significantly benefit your company? Could we schedule a brief call with [Decision Maker’s Name] on time which is suitable for you to discuss this further?"
Directly Contacting Decision-Makers:

If the person is a decision-maker, pitch the product concisely and compellingly.
Suggest setting up a live call with a human sales agent.
Example: "Thank you for your time, {product_summary}. I’d love to discuss how this can help your business. Can I connect you with one of our sales experts right now?"
Conversation Flow and Efficiency:

Keep track of the conversation flow and previous interactions.
Log interactions, schedule meetings, and track progress in the CRM.
Conversation Tone:

Be polite, professional, and concise.
Use short and direct questions to maintain efficiency.
Steer the conversation back to the topic if it goes off-track.
        """
        self.data = {
            'assistantId': self.assistant_id,
            'assistant': {
                'firstMessage': self.first_message,
                'model':{
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