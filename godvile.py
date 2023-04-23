import requests
import json

def get_hero(god_name: str) -> tuple[dict,int]:
    resp = requests.get(f"https://godville.net/gods/api/{god_name}")
    return json.loads(resp.text), resp.status_code

def get_hero(god_name: str, token: str) -> tuple[dict,int]:
    resp = requests.get(f"https://godville.net/gods/api/{god_name}/{token}")
    hero = json.loads(resp.text)
    if "health" in hero:
        return hero, resp.status_code
    else:
        return hero, 403
