import os
import requests

def run_translate_ko_to_en(source:str, target:str,sentence:str):

    URL = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    headers = {
        "charset": "utf-8",
        "X-NCP-APIGW-API-KEY-ID": os.environ["CLIENT_ID"],
        "X-NCP-APIGW-API-KEY": os.environ["CLIENT_SECRET"],
    }
    data = {
        "source": source,  # ko ,en
        "target": target,  # en, ko
        "text": sentence,
    }
    response = requests.post(URL, headers=headers, json=data)
    translated_text = (
        response.json().get("message", {}).get("result", {}).get("translatedText")
    )

    return translated_text
