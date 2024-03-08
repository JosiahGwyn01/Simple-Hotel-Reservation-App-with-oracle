import random

# Sample room types and their corresponding rates
room_types = ["standard", "deluxe", "suite"]
rate_ranges = {
    "standard": (100, 200),
    "deluxe": (250, 350),
    "suite": (400, 650)
}

# Generate 50 entries with random rates and room types
entries = []
for _ in range(300):
    room_type = random.choice(room_types)
    rate = round(random.uniform(rate_ranges[room_type][0], rate_ranges[room_type][1]), 2)
    room_capacity = random.randint(1, 4)
    entry = (room_type, rate, room_capacity)  # Exclude room_number for now
    entries.append(entry)

# Sort the entries by room type (standard, deluxe, suite)
entries.sort(key=lambda x: room_types.index(x[0]))

# Generate room numbers sequentially (001, 002, etc.)
for i, entry in enumerate(entries, start=1):
    room_number = f"{i:03}"  # Use f-string to format the room number
    entry = (room_number,) + entry  # Add the room_number to the entry
    entries[i-1] = entry  # Replace the original entry with the one including room_number

# Display the generated entries with INSERT statements
for entry in entries:
    print("INSERT INTO Room (Room_Number, Room_Type, Rate, room_capacity)")
    print(f"VALUES {entry};")
