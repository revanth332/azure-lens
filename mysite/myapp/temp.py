import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import requests
import uuid

load_dotenv()
cog_end = os.getenv('TRANSLATE_END')
cog_key = os.getenv('TRANSLATE_kEY')
cog_reg = os.getenv('COG_SERVICE_REG')
path = 'translate'
url = cog_end + path

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': ['fr']
}

headers = {
    'Ocp-Apim-Subscription-Key': cog_key,
    'Ocp-Apim-Subscription-Region': cog_reg,
    'Content-type': 'application/json'
}

body = [{
    'text': "Hello how are you?"
}]

# Send the request and get response
request = requests.post(url, params=params, headers=headers, json=body)
response = request.json()

# Parse JSON array and get translation
translation = response[0]["translations"][0]["text"]
print(translation)