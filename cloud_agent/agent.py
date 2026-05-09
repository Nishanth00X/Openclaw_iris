import os
import requests

# Configuration
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
CHAT_ID = "8238216263"
REPO_PATH = "/home/nishanthan/.openclaw/workspace"

def get_latest_git_msg():
    try:
        import subprocess
        result = subprocess.check_output(
            ["git", "-C", REPO_PATH, "log", "-1", "--pretty=%B"],
            stderr=subprocess.STDOUT,
            text=True
        )
        return result.strip()
    except Exception as e:
        return f"Error reading git log: {e}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def query_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Groq Error: {e}"

def main():
    msg = get_latest_git_msg()
    if "Automated memory sync" in msg:
        summary = query_groq(f"Summarize this update in one punchy sentence: {msg}")
        send_telegram_message(f"🚀 *Cloud Agent Alert*\n\nI've detected a sync update!\n\n*Summary:* {summary}")
    else:
        send_telegram_message("☁️ *Cloud Agent Active*\nMonitoring repository for updates...")

if __name__ == "__main__":
    main()
