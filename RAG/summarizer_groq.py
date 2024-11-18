from groq import Groq
from PyPDF2 import PdfReader
groq = Groq(api_key="")

def llama_summarize_content(content):
    prompt = "You are a summarizer based on the given file and context summarize the file relevant to the context"

    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"this is the content{content}"
            }
        ],
        model="llama-3.2-1b-preview"
    )
    return chat_completion[0].message.content

def llama_get_category(content):
    prompt = "You are a categorezier based on the query you will categorize the query in one of three types 1) product_case_study 2) asking_for_product 3) other , return a json with key being type and value being the type of query"
    chat_completion = groq.char.completions.create(
        messages=[
            {
                "role":"system",
                "content":prompt
            },
            {
                "role":"user",
                "content":content
            }
        ],
        model="llama-3.2-1b-preview",
        response_format={"type": "json_object"},
    )
    return chat_completion.choices[0].message.content
def get_file(file_path):
    reader = PdfReader(file_path)
    text = ""
    for i in range(len(reader.pages)):
        page =  reader.pages[i]
        text += page.extract_text()
    return text

