import sys
import json
import os
import requests

API_ENDPOINT = os.getenv("host")
AUTH_TOKEN = os.getenv("token")
if API_ENDPOINT.endswith("/"):
    API_ENDPOINT = API_ENDPOINT[:-1]

def send_memo(content):
    url = f"{API_ENDPOINT}/api/v1/memo"
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    visibility = sys.argv[1]
    data = {
        "content": content,
        "visibility": visibility,
        "resourceIdList": []
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending the memo:")
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Error Details: {e}")
        print(f"Response Content: {e.response.text if e.response else 'No response content'}")
        return None

def main():
    content = sys.argv[2] 
    result = send_memo(content)
        
    if result and (result.get("data", {}).get("id") or result.get("id")):
        print(f"Memo sent successfully")
    else:
        print(f"Failed to send memo")

if __name__ == "__main__":
    main()