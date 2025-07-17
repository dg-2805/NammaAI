import requests

API_KEY = "AIzaSyAkP7wIf9NEhYwItOP45wkaxiT1KFW6Hlw"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [
        {
            "parts": [{"text": "Tell me a fun fact about Bangalore"}]
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.text)
