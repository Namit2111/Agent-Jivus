import requests
from bs4 import BeautifulSoup
import json
from config import HEADERS,NEBULA_API,OPEN_AI_KEY
from openai import OpenAI
import os
openai = OpenAI(api_key=OPEN_AI_KEY)

def check_linkedin_json(url):
    json_file = "linkedinSummaryAiagent.json"
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            summaries = json.load(file)

    else:
        summaries = {}
    if url in summaries:
        return True,summaries[url]
    return False,None

def check_website_json(url):
    json_file = "websiteSummaryAiagent.json"
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            summaries = json.load(file)

    else:
        summaries = {}
    if url in summaries:
        return True,summaries[url]
    return False,None
def get_linkedin_profile_nubela(linkedin_url):
    if True:
        headers = {"Authorization": "Bearer " + NEBULA_API}
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        params = {
            "linkedin_profile_url": linkedin_url,
            "fallback_to_cache": "on-error",
            "use_cache": "if-present",
            "skills": "exclude",
            "inferred_salary": "exclude",
            "personal_email": "exclude",
            "personal_contact_number": "exclude",
            "twitter_profile_id": "exclude",
            "facebook_profile_id": "exclude",
            "github_profile_id": "exclude",
            "extra": "exclude",
        }

        response = requests.get(api_endpoint, params=params, headers=headers)
        response = response.json()
        with open("data.json", "w"):
            json.dump(response, open("data.json", "w"))
        # print(response)
        if response.get("code", 200) != 200:
            raise Exception(f"Error in getting LinkedIN profile: {response}")
    else:
        with open(
            join(config["PROMPTS_PATH"], "sample_linkedin_profile.json"), "r"
        ) as f:
            response = json.load(f)
    return response


def get_linkedin_summary(url):
    flag,data  = check_linkedin_json(url)
    if flag:
        return data
        
    profile = get_linkedin_profile_nubela(linkedin_url=url)
    linkedin_summary_prompt = """  
    You are a top behavior analyst. You are an expert at analyzing LinkedIn profiles based on the DISC framework and figuring out their personality traits and buying styles.

I want you to accurately identify the buying style and personality summary from the LinkedIn data provided below.

Important rules:
- Be direct. Don't mention DISC anywhere in your answer.
- I'm not interested in knowing how you derive your answer.
- Make sure your answer is not more than 100 words.

Here is the LinkedIn profile data:
{}
    
    """.format(profile)


    schema = {
    "type": "object",
    "properties": {
        "personality_summary": {
            "type": "string",
            "description": "Provide the buying style and personality summary from the LinkedIn data provided. Limit the summary to less than 100 words"
        }
    },
    "required": ["personality_summary"]
}   


    messages = [
        {"role": "system", "content": "you are a virtual assistant"},
        {"role": "user", "content": linkedin_summary_prompt},
    ]




    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_response",
                "parameters": schema,
            },
        }
    ]



    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,  # type: ignore
        tools=tools,  # type: ignore
        tool_choice={"type": "function", "function": {"name": "generate_response"}},
    )
    raw_data_str = completion.choices[0].message.tool_calls[0].function.arguments
    llm_response = json.loads(raw_data_str)
    summary =  llm_response["personality_summary"]
    json_file = "linkedinSummaryAiagent.json"
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            summaries = json.load(file)
    else:
        summaries = {}
    
    summaries[url] = summary
    
    with open(json_file, "w") as file:
        json.dump(summaries, file, indent=4)
    

    return summary


# print(get_linkedin_summary("https://www.linkedin.com/in/namit2111/"))


def extract_text_from_website(url):
    # Needed incase of Access Denied
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.content, "lxml")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text



def get_website_summary(url):

    flag,data  = check_website_json(url)
    if flag:
        return data
    website_text = extract_text_from_website(url)
    website_summary_prompt = """ 
    You are an expert business analyst. You have an exceptional knack for just looking at websites and quickly getting an accurate understanding of their business.

Task: I will feed you website data and you will provide brief description of what's their business, like what do they do, how they do it, what product or services they offer, what are their features/benefits, what problems are they solving and what really makes them better than the competition.

Keep it under 50 words.

Here is the website data:
{}
    """.format(website_text)


    messages = [
        {"role": "system", "content": "you are a virtual assistant"},
        {"role": "user", "content": website_summary_prompt},
    ]
#     schema = {
#     "type": "object",
#     "properties": {
#         "product_description": {
#             "type": "string",
#             "description": "Provide the response which is explained in Task"
#         }
#     },
#     "required": ["product_description"]
# }

    schema = {
    "type": "object",
    "properties": {
        "product_name": {
            "type": "string",
            "description": "The name of the product"
        },
        "product_description": {
            "type": "string",
            "description": "Provide the response which is explained in Task"
        }
    },
    "required": ["product_name", "product_description"]


    }
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_response",
                "parameters": schema,
            },
        }
    ]
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,  # type: ignore
        tools=tools,  # type: ignore
        tool_choice={"type": "function", "function": {"name": "generate_response"}},
        temperature=1.5,
        top_p=0.7,
        frequency_penalty=0.2,
        presence_penalty=0.2,
    )
    raw_data_str = completion.choices[0].message.tool_calls[0].function.arguments
    llm_response = json.loads(raw_data_str)
    website_summary = llm_response["product_description"]
    website_name = llm_response["product_name"]
    json_file = "websiteSummaryAiagent.json"
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            summaries = json.load(file)
    else:
        summaries = {}
    
    summaries[url] = {
        "product_name": website_name,
        "product_description": website_summary
    }
    
    with open(json_file, "w") as file:
        json.dump(summaries, file, indent=4)
    return {
        "product_name": website_name,
        "product_description": website_summary
    }
print(get_website_summary("https://www.flipkart.com/tyy/4io/~cs-6ky41lperx/pr?sid=tyy%2C4io&collection-tab-name=POCO+M6+Pro+5G&param=3243&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InZhbHVlQ2FsbG91dCI6eyJtdWx0aVZhbHVlZEF0dHJpYnV0ZSI6eyJrZXkiOiJ2YWx1ZUNhbGxvdXQiLCJpbmZlcmVuY2VUeXBlIjoiVkFMVUVfQ0FMTE9VVCIsInZhbHVlcyI6WyJGcm9tIOKCuTksMjQ5KiJdLCJ2YWx1ZVR5cGUiOiJNVUxUSV9WQUxVRUQifX0sInRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIlBvY28gTTYgUHJvIDVHIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fSwiaGVyb1BpZCI6eyJzaW5nbGVWYWx1ZUF0dHJpYnV0ZSI6eyJrZXkiOiJoZXJvUGlkIiwiaW5mZXJlbmNlVHlwZSI6IlBJRCIsInZhbHVlIjoiTU9CR1JOWjNGWDVYTlIyVCIsInZhbHVlVHlwZSI6IlNJTkdMRV9WQUxVRUQifX19fX0%3D")["product_name"])




def get_calls():
    response = requests.get("https://api.vapi.ai/call", headers=HEADERS) 
    return response