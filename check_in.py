import tkinter as tk
import cx_Oracle
import uuid
from tkinter import messagebox
from tkinter import ttk


def enter_details():
    global fullname_entry, dob_entry, mob_entry, yob_entry, address_entry, mobile_entry, room_number_entry, days_entry, check_in_window

    check_in_window = tk.Toplevel()
    check_in_window.title("Check-in")
    check_in_window.geometry("300x500")
    check_in_window.configure(background="#FFDAB9")
    
    # Entry fields for user input
    fullname_label = tk.Label(check_in_window, text="Full Name:")
    fullname_label.pack(pady=(10, 0))
    fullname_entry = tk.Entry(check_in_window)
    fullname_entry.pack()

    dob_label = tk.Label(check_in_window, text="Date of Birth (DD):")
    dob_label.pack(pady=(10, 0))
    dob_entry = tk.Entry(check_in_window)
    dob_entry.pack()

    mob_label = tk.Label(check_in_window, text="Month of Birth (MM):")
    mob_label.pack(pady=(10, 0))
    mob_entry = tk.Entry(check_in_window)
    mob_entry.pack()

    yob_label = tk.Label(check_in_window, text="Year of Birth (YYYY):")
    yob_label.pack(pady=(10, 0))
    yob_entry = tk.Entry(check_in_window)
    yob_entry.pack()

    address_label = tk.Label(check_in_window, text="Address:")
    address_label.pack(pady=(10, 0))
    address_entry = tk.Entry(check_in_window)
    address_entry.pack()

    mobile_label = tk.Label(check_in_window, text="Mobile Number:")
    mobile_label.pack(pady=(10, 0))
    mobile_entry = tk.Entry(check_in_window)
    mobile_entry.pack()

    room_number_label = tk.Label(check_in_window, text="Room Number:")
    room_number_label.pack(pady=(10, 0))
    room_number_entry = tk.Entry(check_in_window)
    room_number_entry.pack()

    days_label = tk.Label(check_in_window, text="Number of Days:")
    days_label.pack(pady=(10, 0))
    days_entry = tk.Entry(check_in_window)
    days_entry.pack()

    def display_available_rooms():
        try:
            # Establish a connection to the Oracle database
            dsn = cx_Oracle.makedsn("localhost", 1521, "orcl")
            connection = cx_Oracle.connect("sys", "orcl", dsn, mode=cx_Oracle.SYSDBA) 

            # Retrieve available rooms sorted by room number
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Room_Number, Room_Type, Rate FROM Room 
                    WHERE Room_Number NOT IN (
                        SELECT Room_Number FROM Stay
                    )
                    ORDER BY Room_Number
                    """)
                available_rooms = cursor.fetchall()

            # Create a new window for displaying the available rooms
            available_rooms_window = tk.Toplevel()
            available_rooms_window.title("Available Rooms")

            # Create a Treeview widget
            tree = ttk.Treeview(available_rooms_window)
            tree["columns"] = ("Room_Number", "Room_Type", "Rate")
            tree.heading("Room_Number", text="Room Number")
            tree.heading("Room_Type", text="Room Type")
            tree.heading("Rate", text="Rate")

                # Insert data into the Treeview
            for row in available_rooms:
                tree.insert("", tk.END, values=row)

            # Pack the Treeview and configure it
            tree.pack(fill=tk.BOTH, expand=True)
            tree.column("#0", width=0, stretch=tk.NO)  # Hide the first column

        except cx_Oracle.DatabaseError as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")

        finally:
                # Close the connection
            connection.close()


    def submit_check_in():
        # Get user input from entry fields
            fullname = fullname_entry.get()
            dob = int(dob_entry.get())
            mob = int(mob_entry.get())
            yob = int(yob_entry.get())
            address = address_entry.get()
            mobile_number = mobile_entry.get()
            room_number = room_number_entry.get()
            number_days = days_entry.get()
            date_of_birth = cx_Oracle.Date(yob, mob, dob)

            try:
                # Establish a connection to the Oracle database
                dsn = cx_Oracle.makedsn("localhost", 1521, "orcl")
                connection = cx_Oracle.connect("sys", "orcl", dsn, mode=cx_Oracle.SYSDBA)

                # Generate a random guest ID
                initialGuest_id = str(uuid.uuid4())
                guest_id = int(initialGuest_id.replace("-", ""), 16)

                # Insert data into the Guests table
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Guest (Guest_ID, Name, Date_of_Birth, Address, Phone_Number)
                        VALUES (:guest_id, :fullname, :date_of_birth, :address, :mobile_number)
                    """, guest_id=guest_id, fullname=fullname, date_of_birth=date_of_birth, address=address, mobile_number=mobile_number)
                    connection.commit()

                    # Retrieve the rate for the selected room from the Room table
                    cursor.execute("SELECT Rate FROM Room WHERE Room_Number = :1", (room_number,))
                    rate = cursor.fetchone()

                    # Calculate the total fees
                    total_fees = int(rate[0]) * int(number_days)

                    # Insert data into the Stay table
                    cursor.execute("""
                        INSERT INTO Stay (Guest_ID, Room_Number, Number_of_Days, Fees)
                        VALUES (:guest_id, :room_number, :number_days, :total_fees)
                    """, guest_id=guest_id, room_number=room_number, number_days=number_days, total_fees=total_fees)
                    connection.commit()

                    # Show a receipt window with the check-in details and fees
                    receipt_window = tk.Toplevel()
                    receipt_window.title("Check-in Receipt")
                    receipt_window.geometry("300x200")
                    receipt_window.configure(background="#FFDAB9")

                    receipt_label = tk.Label(receipt_window, text="Check-in Receipt")
                    receipt_label.pack(pady=(10, 0))

                    receipt_details = f"Full Name: {fullname}\nRoom Number: {room_number}\nNumber of Days: {number_days}\nTotal Fees: {total_fees}"
                    receipt_text = tk.Label(receipt_window, text=receipt_details)
                    receipt_text.pack(pady=(10, 0))

                    def return_to_main_menu():
                        receipt_window.destroy()
                        check_in_window.destroy()

                    def edit_entries():
                        receipt_window.destroy()

                    # OK button to return to the main menu
                    ok_button = tk.Button(receipt_window, text="OK", command=return_to_main_menu)
                    ok_button.pack(pady=(10, 0))

                    # Cancel button to edit entries
                    cancel_button = tk.Button(receipt_window, text="Cancel", command=edit_entries)
                    cancel_button.pack(pady=(10, 0))

            except cx_Oracle.DatabaseError as error:
                messagebox.showerror("Database Error", f"An error occurred: {error}")

            finally:
                # Close the connection
                connection.close()


        # Available Rooms button
    available_rooms_button = tk.Button(check_in_window, text="Available Rooms", command=display_available_rooms)
    available_rooms_button.pack(pady=(20, 10))

        # Submit button
    submit_button = tk.Button(check_in_window, text="Submit", command=submit_check_in)
    submit_button.pack()

if __name__ == "__main__":
    enter_details()
