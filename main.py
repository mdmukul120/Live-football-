import os
import http.client
import json
from datetime import datetime

# GitHub Secrets / Environment Variable থেকে API Key গ্রহণ
API_KEY = os.getenv("RAPIDAPI_KEY")

# API Host এর নাম
API_HOST = "free-api-live-football-data.p.rapidapi.com"

def fetch_api_data(endpoint):
    """
    RapidAPI থেকে নির্দিষ্ট এন্ডপয়েন্টের ডাটা ফেচ করার ফানশন
    """
    if not API_KEY:
        print("Error: RAPIDAPI_KEY পাওয়া যায়নি! দয়া করে Environment Variable সেট করুন।")
        return None

    try:
        conn = http.client.HTTPSConnection(API_HOST)
        headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': API_HOST,
            'Content-Type': "application/json"
        }
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None

def main():
    print(f"[{datetime.now()}] Data fetching process started...")

    # ডাটা সংরক্ষণের জন্য 'data' ফোল্ডার তৈরি (যদি না থাকে)
    os.makedirs("data", exist_ok=True)

    # ১. প্লেয়ার তথ্য ফেচ করা
    print("Fetching player data...")
    endpoint = "/football-players-search?search=m"
    players_data = fetch_api_data(endpoint)

    if players_data:
        file_path = "data/players.json"
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(players_data, file, ensure_ascii=False, indent=4)
        print(f"Successfully updated and saved data to {file_path}")
    else:
        print("Failed to fetch or save player data.")

if __name__ == "__main__":
    main()
