import datetime
import json
import argparse
import os
import cryptography.fernet as fernet


argument_parser = argparse.ArgumentParser(description="Simple timecapsule.")

subparsers = argument_parser.add_subparsers(dest="command", required=True)

create_parser = subparsers.add_parser("create", help="Create a new time capsule.")
create_parser.add_argument("-o", "--open-at", type=str, required=True, help="Date to open the time capsule (YYYY-MM-DD).")
create_parser.add_argument("-m", "--message", type=str, required=True, help="Message to store in the time capsule.")

list_parser = subparsers.add_parser("list", help="List saved timecapsules.")

show_parser = subparsers.add_parser("show", help="Show details of a specific time capsule by date.")
show_parser.add_argument("date", type=str, help="Date of the time capsule to show (YYYY-MM-DD).")

open_parser = subparsers.add_parser("open", help="Open the time capsule if the date has passed.")
open_parser.add_argument("date", type=str, help="Date of the time capsule to open (YYYY-MM-DD).")

delete_parser = subparsers.add_parser("delete", help="Delete a specific time capsule by date.")
delete_parser.add_argument("date", type=str, help="Date of the time capsule to delete (YYYY-MM-DD).")

args = argument_parser.parse_args()

print("\t\tTerminal Timecapsule")
print("------------------------------------------------------")


def encrypt_message(message):
    if not os.path.exists("capsule_keys.key"):
        key = fernet.Fernet.generate_key()
        with open("capsule_keys.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("capsule_keys.key", "rb") as key_file:
            key = key_file.read()

    cipher = fernet.Fernet(key)
    message = message.encode()
    encrypted_message = cipher.encrypt(message)

    return encrypted_message

def decrypt_message(encrypted_message):
    try:
        with open("capsule_keys.key", "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        print("Encryption key not found.")
        return None

    cipher = fernet.Fernet(key)
    decrypted_message = cipher.decrypt(encrypted_message.encode())

    return decrypted_message.decode()

def load_timecapsules():
    try:
        with open("timecapsules.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def create_timecapsule(open_at, message):
    encrypted_message = encrypt_message(message)
    capsule = {
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "open_at": open_at.strftime("%Y-%m-%d"),
        "message": encrypted_message.decode()
    }
    capsules = load_timecapsules()
    capsules.append(capsule)
    with open("timecapsules.json", "w") as f:
        json.dump(capsules, f, indent=4)


def list_timecapsules():
    try:
        with open("timecapsules.json", "r") as f:
            capsules = json.load(f)
            for capsule in capsules:
                if datetime.datetime.now() >= datetime.datetime.strptime(capsule["open_at"], "%Y-%m-%d"):
                    print(f"\033[32mDate: {capsule['open_at']}, Created On: {capsule['created_at']} (Ready to Open)\033[0m")
                else:
                    print(f"Date: {capsule['open_at']}, Created On: {capsule['created_at']}")
    except FileNotFoundError:
        print("No time capsules found.")
    
def show_timecapsule(date):
    capsules = load_timecapsules()
    found = False
    for capsule in capsules:
        if capsule["open_at"] == date.strftime("%Y-%m-%d"):
            print(f"Date: {capsule['open_at']}, Created On: {capsule['created_at']}")
            found = True
    if not found:
        print("Time capsule not found.")

def open_timecapsule(date):
    capsules = load_timecapsules()
    found = False
    for capsule in capsules:
        if capsule["open_at"] == date.strftime("%Y-%m-%d"):
            if datetime.datetime.now() >= date:
                decrypted_msg = decrypt_message(capsule["message"])
                if decrypted_msg:
                    print(f"Created On: {capsule['created_at']}")
                    print(f"Message: {decrypted_msg}")
                    print("----------------------------")
            else:
                print("This time capsule cannot be opened yet.")
            found = True
    if not found:
        print("Time capsule not found.")

def delete_timecapsule(date):
    capsules = load_timecapsules()
    capsules_on_date = [c for c in capsules if c['open_at'] == date.strftime("%Y-%m-%d")]

    if not capsules_on_date:
        print("Time capsule not found.")
        return
    
    if len(capsules_on_date) > 1:
        print("Multiple time capsules found for this date. Specify which one to delete.")
        for i in capsules_on_date:
            print(f"Created On: {i['created_at']}, Open At: {i['open_at']}")
            print("----------------------------------------------------------")
        choice = int(input("Enter the number of the time capsule to delete or 0 for all:"))
        if choice == 0:
            capsules = [c for c in capsules if c['open_at'] != date.strftime("%Y-%m-%d")]
        else:
            to_delete = capsules_on_date[choice - 1]
            capsules.remove(to_delete)
    else:
        capsules = [c for c in capsules if c['open_at'] != date.strftime("%Y-%m-%d")]

    with open("timecapsules.json", "w") as f:
        json.dump(capsules, f, indent=4)



if args.command == "create":
    open_at_date = datetime.datetime.strptime(args.open_at, "%Y-%m-%d")
    create_timecapsule(open_at_date, args.message)
    print("Time capsule created.")
elif args.command == "list":
    list_timecapsules()
elif args.command == "show":
    date = datetime.datetime.strptime(args.date, "%Y-%m-%d")
    show_timecapsule(date)
elif args.command == "open":
    date = datetime.datetime.strptime(args.date, "%Y-%m-%d")
    open_timecapsule(date)
elif args.command == "delete":
    date = datetime.datetime.strptime(args.date, "%Y-%m-%d")
    delete_timecapsule(date)