from groq import Groq
from PyPDF2 import PdfReader
import json
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
                "content": "".format(content)
            }
        ],
        model="llama-3.2-1b-preview"
    )
    return chat_completion.choices[0].message.content

def llama_get_category(content):
    prompt = "You are a categorezier based on the query you will categorize the query in one of three types 1) product_case_study 2) asking_for_product 3) other , return a json with key being type and value being the type of query"
    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role":"system",
                "content":prompt
            },
            {
"role":"system",
"content":"you have only three types of categories product_case_study, asking_for_product, other"
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

if __name__ == "__main__":
    d = llama_get_category(content="what is your product")
    d_dict = json.loads(d)
    type_value = d_dict["type"]
    print(json.loads(d)['type'])