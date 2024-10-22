import requests
from openai import AzureOpenAI
from config import AZURE_API_KEY,AZURE_ENDPOINT,AZURE_MODEL,AZURE_API_VER
def get_chat_completion(user_message):
  client = AzureOpenAI(
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VER,
        azure_endpoint=AZURE_ENDPOINT,
    )

  completion = client.chat.completions.create(
        model=AZURE_MODEL,
        messages=[
            {
                "role": "user",
                "content": user_message,
            },
        ],
    )
    
    # Return the JSON response
  return completion

if __name__ == "__main__":
    endpoint = "https://example-endpoint.openai.azure.com"  # Replace with your endpoint
    deployment_name = "deployment-name"  # Replace with your deployment name
    user_message = "Tell me that your name is sez"

    result = get_chat_completion(user_message)
