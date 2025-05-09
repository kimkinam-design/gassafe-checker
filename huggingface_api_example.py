import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/kimkinam-design"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "inputs": "검사 대상 예시 입력 문장입니다."
}

response = requests.post(API_URL, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response:", response.text)
