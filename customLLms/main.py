from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from call_azure_bot import get_chat_completion
import json

app = FastAPI()

async def generate_response(data):
    for choice in data.choices:
        chunk = choice.message.content
        json_data = json.dumps({
            'choices': [
                {
                    'delta': {
                        'content': chunk,
                        'role': 'assistant'
                    }
                }
            ]
        })
        yield f"data: {json_data}\n\n"
    
    yield "data: [DONE]\n\n"

@app.post("/chat/completions")
async def basic_custom_llm_route(request: Request):
    request_data = await request.json()
    messages = request_data.get("messages", [])
    human_message_content = None
    for message in messages:
        if message.get("role") == "user":
            human_message_content = message.get("content")
    data =  get_chat_completion(user_message=human_message_content)
    return StreamingResponse(generate_response(data), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
