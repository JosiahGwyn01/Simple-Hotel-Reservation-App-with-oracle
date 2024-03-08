import random
import uuid

# Sample addresses
addresses = [
    "123 Main Street",
    "456 Elm Avenue",
    "789 Oak Road",
    "321 Pine Lane",
    "555 Maple Drive",
]

# Sample names
names = [
    "John Smith",
    "Alice Johnson",
    "Michael Williams",
    "Emily Brown",
    "James Jones",
]

# Sample room numbers (1 to 300)
room_numbers = list(range(1, 301))

# Generate 50 guest entries with random details
guest_entries = []
used_guest_ids = set()  # To keep track of used guest IDs
for _ in range(100):
    while True:
        guest_id = random.randint(10000, 99999)  # Generate a random guest ID as an integer
        if guest_id not in used_guest_ids:
            used_guest_ids.add(guest_id)
            break

    # Rest of the code remains the same
    name = random.choice(names)
    date_of_birth = f"{random.randint(1950, 2003)}-{random.randint(1, 12):02}-{random.randint(1, 28):02}"
    address = random.choice(addresses)
    phone_number = f"({random.randint(100, 999)})-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    entry = (guest_id, name, date_of_birth, address, phone_number)
    guest_entries.append(entry)

# Generate Stay entries for each guest entry with a random Room_Number and Number_of_Days
stay_entries = []
used_room_numbers = set()  # To keep track of used room numbers
for entry in guest_entries:
    guest_id = entry[0]

    while True:
        room_number = random.choice(room_numbers)
        if room_number not in used_room_numbers:
            used_room_numbers.add(room_number)
            break

    number_of_days = random.randint(1, 5)
    fees = random.randint(100, 1000)

    stay_entry = (guest_id, room_number, number_of_days, fees)
    stay_entries.append(stay_entry)

# Display the generated entries in SQL format
for entry in guest_entries:
    guest_id, name, date_of_birth, address, phone_number = entry
    print("INSERT INTO Guest (Guest_ID, Name, Date_of_Birth, Address, Phone_Number) VALUES")
    print(f"('{guest_id}', '{name}', DATE '{date_of_birth}', '{address}', '{phone_number}');")
    print("")

    # Find the corresponding stay entry for this guest
    for stay_entry in stay_entries:
        if stay_entry[0] == guest_id:
            guest_id, room_number, number_of_days, fees = stay_entry
            print("INSERT INTO Stay (Guest_ID, Room_Number, Number_of_Days, Fees) VALUES")
            print(f"('{guest_id}', {room_number}, {number_of_days}, {fees});")
            print("")

            break  # Found the corresponding stay entry, break the loop

