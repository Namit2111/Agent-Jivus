import os
import json
from datetime import datetime
from groq import Groq

groq = Groq(
    api_key="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",
)

# now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# persona = "Teemu"
# home_location = "Madrid"
schema = memory_schema = {
  "type": "object",
  "properties": {
    "query_answer": {
      "type": "string",
      "description": "This will be the answer to the user query"
    },
    
  }
}
prompt_by_user = "Today was sunny day and then rained, I went to city to have a dinner with friends and I ate the best Sushi I have ever tested in restaurant called Sushita Cafe, where my friend Paco is a chef."

chat_completion = groq.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": f"You are helpful memory recorder.\nWrite outputs in JSON in schema: {schema}.\nCurrent time is {now}.\nI am {persona} living in {home_location} and events may take place in more specific places inside the home location or outside it, so record precisely.\n",
            #"content": "You are helpful memory recorder. Write outputs in JSON schema.\n",
            #f" The JSON object must use the schema: {json.dumps(my_schema.model_json_schema(), indent=1)}",
        },
        {
            "role": "user",
            "content": "Today was sunny day and then rained, I went to city to have a dinner with friends and I ate the best Sushi I have ever tested in restaurant called Sushita Cafe, where my friend Paco is a chef.",
        }
    ],
    model="llama-3.2-1b-preview",
    response_format={"type": "json_object"},
)
print(chat_completion.choices[0].message.content)