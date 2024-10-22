from dotenv import load_dotenv
import os 
load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_MODEL = os.getenv('AZURE_MODEL')
AZURE_API_VER = os.getenv('AZURE_API_VER')