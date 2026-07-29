import json
import csv
import re
import os
from datetime import datetime

FILE_NAME = "contacts_data.json"
BACKUP_FILE = "contacts_backup.json"


# ----------------------------
# Validation Functions
# ----------------------------

def validate_phone(phone):
    digits = re.sub(r"\D", "", phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None


def validate_email(email):
    if email == "":
        return True
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


# ----------------------------
# File Functions
# ----------------------------

def save_contacts(contacts):
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)

    with open(BACKUP_FILE, "w") as file:
        json.dump(contacts, file, indent=4)


def load_contacts():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return {}
    return {}


# ----------------------------
# CRUD Functions
# ----------------------------

def add_contact(contacts):

    name = input("Enter Name: ").strip().title()

    if not name:
        print("Name cannot be empty.")
        return

    if name in contacts:
        print("Contact already exists.")
        return

    while True:
        phone = input("Enter Phone: ")
        valid, phone = validate_phone(phone)

        if valid:
            break
        print("Invalid phone number.")

    while True:
        email = input("Enter Email (optional): ")

        if validate_email(email):
            break
        print("Invalid Email.")

    address = input("Enter Address: ")
    group = input("Group (Friends/Work/Family/Other): ")

    contacts[name] = {
        "phone": phone,
        "email": email,
        "address": address,
        "group": group if group else "Other",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    save_contacts(contacts)
    print("Contact Added Successfully.")


def search_contact(contacts):

    keyword = input("Search Name: ").lower()

    found = False

    for name, details in contacts.items():
        if keyword in name.lower():
            print("-" * 40)
            print("Name :", name)
            print("Phone:", details["phone"])
            print("Email:", details["email"])
            print("Address:", details["address"])
            print("Group:", details["group"])
            found = True

    if not found:
        print("No contact found.")


def search_phone(contacts):

    number = re.sub(r"\D", "", input("Phone Number: "))

    for name, details in contacts.items():
        if details["phone"] == number:
            print(name, details)
            return

    print("No contact found.")


def update_contact(contacts):

    name = input("Contact Name: ").title()

    if name not in contacts:
        print("Contact not found.")
        return

    print("Leave blank to keep old value.")

    phone = input("Phone: ")

    if phone:
        valid, phone = validate_phone(phone)

        if valid:
            contacts[name]["phone"] = phone

    email = input("Email: ")

    if email:
        if validate_email(email):
            contacts[name]["email"] = email

    address = input("Address: ")

    if address:
        contacts[name]["address"] = address

    group = input("Group: ")

    if group:
        contacts[name]["group"] = group

    contacts[name]["updated_at"] = datetime.now().isoformat()

    save_contacts(contacts)

    print("Contact Updated.")


def delete_contact(contacts):

    name = input("Enter Name: ").title()

    if name not in contacts:
        print("Contact not found.")
        return

    confirm = input("Delete Contact? (Y/N): ")

    if confirm.lower() == "y":
        del contacts[name]
        save_contacts(contacts)
        print("Deleted Successfully.")


def display_contacts(contacts):

    if not contacts:
        print("No Contacts.")
        return

    print("\nALL CONTACTS")
    print("=" * 60)

    for name, details in contacts.items():
        print("Name :", name)
        print("Phone:", details["phone"])
        print("Email:", details["email"])
        print("Address:", details["address"])
        print("Group:", details["group"])
        print("-" * 60)


# ----------------------------
# Export CSV
# ----------------------------

def export_csv(contacts):

    with open("contacts.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Name", "Phone", "Email", "Address", "Group"])

        for name, info in contacts.items():
            writer.writerow([
                name,
                info["phone"],
                info["email"],
                info["address"],
                info["group"]
            ])

    print("CSV Exported Successfully.")


# ----------------------------
# Statistics
# ----------------------------

def statistics(contacts):

    print("\nCONTACT STATISTICS")
    print("=" * 30)

    print("Total Contacts:", len(contacts))

    groups = {}

    for info in contacts.values():

        group = info["group"]

        groups[group] = groups.get(group, 0) + 1

    print("\nContacts by Group")

    for g, c in groups.items():
        print(f"{g}: {c}")


# ----------------------------
# Menu
# ----------------------------

def menu():

    contacts = load_contacts()

    while True:

        print("""
==========================
 CONTACT MANAGEMENT SYSTEM
==========================
1.Add Contact
2.Search Contact
3.Update Contact
4.Delete Contact
5.View All
6.Export CSV
7.Statistics
8.Search by Phone
9.Exit
""")

        choice = input("Enter Choice: ")

        if choice == "1":
            add_contact(contacts)

        elif choice == "2":
            search_contact(contacts)

        elif choice == "3":
            update_contact(contacts)

        elif choice == "4":
            delete_contact(contacts)

        elif choice == "5":
            display_contacts(contacts)

        elif choice == "6":
            export_csv(contacts)

        elif choice == "7":
            statistics(contacts)

        elif choice == "8":
            search_phone(contacts)

        elif choice == "9":
            save_contacts(contacts)
            print("Thank You!")
            break

        else:
            print("Invalid Choice.")


if __name__ == "__main__":
    menu()