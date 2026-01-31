import requests
import json
import os
from datetime import datetime

# --- Configuration ---
GH_USERNAME = "rthponder"
CF_HANDLE = "cfponder"
GH_TOKEN = os.getenv("GH_TOKEN") # Fetched from GitHub Secrets

def get_github_data():
    url = 'https://api.github.com/graphql'
    headers = {"Authorization": f"bearer {GH_TOKEN}"}
    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
    variables = {"username": GH_USERNAME}
    try:
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        if response.status_code == 200:
            data = response.json()
            days = []
            weeks = data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
            for week in weeks:
                for day in week['contributionDays']:
                    days.append({"date": day['date'], "value": day['contributionCount']})
            return days
    except Exception as e:
        print(f"GitHub Error: {e}")
    return []

def get_cf_data():
    url = f"https://codeforces.com/api/user.status?handle={CF_HANDLE}"
    try:
        response = requests.get(url).json()
        if response['status'] == 'OK':
            daily_counts = {}
            for sub in response['result']:
                date = datetime.fromtimestamp(sub['creationTimeSeconds']).strftime('%Y-%m-%d')
                daily_counts[date] = daily_counts.get(date, 0) + 1
            return [{"date": d, "value": v} for d, v in daily_counts.items()]
    except Exception as e:
        print(f"Codeforces Error: {e}")
    return []

def main():
    gh_data = get_github_data()
    cf_data = get_cf_data()

    # Merge data by date
    merged = {}
    for entry in gh_data + cf_data:
        d = entry['date']
        merged[d] = merged.get(d, 0) + entry['value']

    # Convert to sorted list for the heatmap
    final_data = [{"date": d, "value": v} for d, v in sorted(merged.items())]

    with open('activity.json', 'w') as f:
        json.dump(final_data, f)

if __name__ == "__main__":
    main()