import requests
from bs4 import BeautifulSoup
import json
from config import HEADERS,NEBULA_API
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


def extract_text_from_website(url):
    HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                           'Accept-Language': 'en-US, en;q=0.5'})
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # soup = BeautifulSoup(response.content, "lxml")
    # print(soup.get_text())
    return soup.get_text()

# get_linkedin_profile_nubela("https://www.linkedin.com/in/namit2111/")

def get_calls():
    response = requests.get("https://api.vapi.ai/call", headers=HEADERS) 
    return response