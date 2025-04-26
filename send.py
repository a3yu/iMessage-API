import json
import requests
import time
from typing import Dict
import os

# Configuration
API_URL = "http://localhost:5000/send"
API_KEY = os.getenv("IMESSAGE_API_KEY")  # Get API key from environment variable
MESSAGES_PER_USER = 5  # Updated to 5 messages
DELAY_BETWEEN_MESSAGES = 1  # seconds between messages to same user
DELAY_BETWEEN_USERS = 2     # seconds between different users

def load_contacts() -> Dict[str, str]:
    with open('contacts.json', 'r') as f:
        return json.load(f)

def get_message_for_sequence(name: str, message_number: int) -> str:
    messages = [
        f"Hey {name}",
        "Hope you are doing well!",
        "Just wanted to thank you again for your support during the elections",
        "If you have time, would you be able to let your friend know that voting for Student Assembly is now available through email and to consider voting David Diao for freshman rep",
        "Thanks so much man!!"
    ]
    return messages[message_number]

def send_message(phone_number: str, name: str, message_number: int) -> bool:
    headers = {
        "api_key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "recipient": name,
        "message": get_message_for_sequence(name, message_number)
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        print(f"Successfully sent message {message_number + 1} to {name} ({phone_number})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message {message_number + 1} to {name} ({phone_number}): {str(e)}")
        return False

def main():
    if not API_KEY:
        print("Error: IMESSAGE_API_KEY environment variable not set")
        return

    contacts = load_contacts()
    
    for phone_number, name in contacts.items():
        print(f"\nSending messages to {name}...")
        
        for i in range(MESSAGES_PER_USER):
            success = send_message(phone_number, name, i)
            
            if success and i < MESSAGES_PER_USER - 1:
                print(f"Waiting {DELAY_BETWEEN_MESSAGES} seconds before next message...")
                time.sleep(DELAY_BETWEEN_MESSAGES)
        
        print(f"Waiting {DELAY_BETWEEN_USERS} seconds before next user...")
        time.sleep(DELAY_BETWEEN_USERS)

if __name__ == "__main__":
    main()
