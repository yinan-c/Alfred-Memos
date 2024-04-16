import sys
import json
import os
import requests


API_ENDPOINT = os.getenv("host")
AUTH_TOKEN = os.getenv("token")
if API_ENDPOINT.endswith("/"):
    API_ENDPOINT = API_ENDPOINT[:-1]

def get_memos():
    url = f"{API_ENDPOINT}/api/v1/memo"
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        memos = response.json()
        return memos
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request:")
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Error Details: {e}")
        print(f"Response Content: {e.response.text if e.response else 'No response content'}")
        return []

def search_memos(query):
    memos = get_memos()
    return [memo for memo in memos if query.lower() in memo["content"].lower()]
import jieba

def generate_alfred_items(memos):
    items = []
    for memo in memos:
        is_comment = any(relation["relatedMemoId"] != memo["id"] for relation in memo.get("relationList", []))
        related_memo_id = next((relation["relatedMemoId"] for relation in memo.get("relationList", []) if relation["type"] == "COMMENT"), None)

        if is_comment:
            related_memo = next((m for m in memos if m["id"] == related_memo_id), None)
            subtitle = f"Comment on: {related_memo['content']}"
            arg = f"{API_ENDPOINT}/m/{related_memo['name']}"
            icon = "comment.png"
        else:
            subtitle = "Memo"
            arg = f"{API_ENDPOINT}/m/{memo['name']}"
            icon = "icon.png"

        content_words = jieba.lcut(memo["content"])
        match_text = ' '.join(content_words) + " " + subtitle

        item = {
            "title": memo["content"],
            "subtitle": subtitle,
            "arg": arg,
            "autocomplete": memo["content"],
            "match": match_text,
            "icon": {
                "path": icon
            },
            "mods": {
                "cmd": {
                    "valid": True,
                    "arg": memo["content"],
                    "subtitle": "Text View",
                },
                "alt": {
                    "valid": True,
                    "arg": memo["content"],
                    "subtitle": "Copy to Clipboard",
                },
            }
        }
        items.append(item)
    return items

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    memos = search_memos(query)
    items = generate_alfred_items(memos)
    output = {"items": items}
    print(json.dumps(output))

if __name__ == "__main__":
    main()
