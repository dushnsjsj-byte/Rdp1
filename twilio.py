import random
from twilio.rest import Client

# Your Twilio credentials (replace with your actual credentials)
ACCOUNT_SID = 'ACa987d5449b76ec09ad033eba95654756'
AUTH_TOKEN = 'ec0a2a59e0270a1615368a6abfa76681'

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def list_active_numbers():
    print("\nActive Twilio Numbers:")
    numbers = client.incoming_phone_numbers.list()
    if not numbers:
        print("No active numbers found.")
    else:
        for num in numbers:
            print(f"SID: {num.sid}, Number: {num.phone_number}")

def buy_new_number(area_code):
    print(f"\nSearching for available Twilio numbers with area code {area_code}...")
    available_numbers = client.available_phone_numbers('US').local.list(area_code=area_code, limit=5)
    if not available_numbers:
        print("No available numbers found for this area code.")
        return
    number_to_buy = available_numbers[0].phone_number
    print(f"Purchasing number: {number_to_buy}")
    purchased_number = client.incoming_phone_numbers.create(phone_number=number_to_buy)
    print(f"Purchased new number: {purchased_number.phone_number}")

def search_sms_logs_by_area_code(area_code):
    print(f"\nSearching SMS logs for area code {area_code}...")
    messages = client.messages.list(limit=50)
    filtered = []
    for msg in messages:
        if (msg.from_ and msg.from_.startswith(f"+1{area_code}")) or (msg.to and msg.to.startswith(f"+1{area_code}")):
            filtered.append(msg)
    if not filtered:
        print("No messages found for this area code.")
    else:
        print(f"Found {len(filtered)} messages:")
        for msg in filtered:
            print(f"From: {msg.from_}, To: {msg.to}, Date: {msg.date_sent}, Body: {msg.body}")

def view_recent_sms_logs(limit=10):
    print(f"\nViewing {limit} most recent SMS logs:")
    messages = client.messages.list(limit=limit)
    if not messages:
        print("No SMS messages found.")
    else:
        for msg in messages:
            print(f"From: {msg.from_}, To: {msg.to}, Date: {msg.date_sent}, Body: {msg.body}")

def main():
    while True:
        print("\nTwilio Account Dashboard")
        print("1. View Active Numbers")
        print("2. Buy New Twilio Number")
        print("3. Search SMS Logs by Area Code")
        print("4. View Recent SMS Logs")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            list_active_numbers()
        elif choice == '2':
            area_code = input("Enter area code for new number (e.g., 650): ").strip()
            if len(area_code) == 3 and area_code.isdigit():
                buy_new_number(area_code)
            else:
                print("Invalid area code. Please enter a 3-digit numeric area code.")
        elif choice == '3':
            area_code = input("Enter area code to search SMS logs (e.g., 650): ").strip()
            if len(area_code) == 3 and area_code.isdigit():
                search_sms_logs_by_area_code(area_code)
            else:
                print("Invalid area code. Please enter a 3-digit numeric area code.")
        elif choice == '4':
            limit_input = input("Enter number of recent SMS logs to view (default 10): ").strip()
            limit = int(limit_input) if limit_input.isdigit() else 10
            view_recent_sms_logs(limit)
        elif choice == '0':
            print("Exiting dashboard.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
