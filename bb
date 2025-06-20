import requests
import json
import os
from datetime import datetime

# === CONFIGURATION ===
JIRA_BASE_URL = "https://your-domain.atlassian.net"
JIRA_API_ENDPOINT = "/rest/api/2/search"
JIRA_EMAIL = "your-email@example.com"
JIRA_API_TOKEN = "your-api-token"
JQL_QUERY = 'project = "XYZA" AND created >= -1d ORDER BY created DESC'

GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/XXXXX/messages?key=XXXX&token=XXXX"

NOTIFIED_ISSUES_FILE = "notified_issues.json"


# === UTILITIES ===

def load_notified_issues():
    if os.path.exists(NOTIFIED_ISSUES_FILE):
        with open(NOTIFIED_ISSUES_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_notified_issues(issue_ids):
    with open(NOTIFIED_ISSUES_FILE, 'w') as f:
        json.dump(list(issue_ids), f)


# === STEP 1: Fetch Issues from Jira ===

def fetch_issues_from_jira(jql):
    url = f"{JIRA_BASE_URL}{JIRA_API_ENDPOINT}"
    headers = {"Content-Type": "application/json"}
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    params = {
        "jql": jql,
        "fields": "key,summary",
        "maxResults": 20
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch Jira issues: {response.status_code} - {response.text}")

    data = response.json()
    return data.get("issues", [])


# === STEP 2: Send to Google Chat ===

def send_to_google_chat(issue_key, summary):
    issue_url = f"{JIRA_BASE_URL}/browse/{issue_key}"
    message = {
        "text": f"🚨 *New Jira Issue Created!*\n*[{issue_key}]({issue_url})*: {summary}"
    }

    response = requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=message)
    if response.status_code != 200:
        print(f"Failed to send message to Google Chat: {response.status_code} - {response.text}")
    else:
        print(f"Sent alert for issue {issue_key}")


# === STEP 3: Main Logic ===

def main():
    try:
        print(f"[{datetime.now()}] Checking for new Jira issues...")
        notified_issues = load_notified_issues()
        issues = fetch_issues_from_jira(JQL_QUERY)

        for issue in issues:
            issue_id = issue["id"]
            issue_key = issue["key"]
            summary = issue["fields"]["summary"]

            if issue_id not in notified_issues:
                send_to_google_chat(issue_key, summary)
                notified_issues.add(issue_id)

        save_notified_issues(notified_issues)
        print("✅ Check completed.\n")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


# === ENTRY POINT ===

if __name__ == "__main__":
    main()
