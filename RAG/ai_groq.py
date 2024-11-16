import os
import json
from datetime import datetime
from groq import Groq

groq = Groq(
    api_key="",
)
schema  = {
  "type":"string"
}
prompt_by_user = "Today was sunny day and then rained, I went to city to have a dinner with friends and I ate the best Sushi I have ever tested in restaurant called Sushita Cafe, where my friend Paco is a chef."

chat_completion = groq.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": f"you are a categorizing agent ,you will categorize the user query in one of three types 1) product_case_study 2) asking_for_product 3) other , return a json with key being type and balue being the type of query",
          
        },
        {
            "role": "user",
            "content": "what is the product name",
        }
    ],
    model="llama-3.2-3b-preview",
    response_format={"type": "json_object"},
)
print(chat_completion.choices[0].message.content)