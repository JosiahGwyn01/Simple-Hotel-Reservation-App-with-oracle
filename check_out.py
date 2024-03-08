import tkinter as tk
import cx_Oracle
import show_current_reservations
from tkinter import messagebox

def show_reservations():
    show_current_reservations.show_current_reservations()

def check_out():
    # Check if the table exists
    table_exists = False
    try:
        # Establish a connection to the Oracle database
        dsn = cx_Oracle.makedsn("localhost", 1521, "orcl")
        connection = cx_Oracle.connect("sys", "orcl", dsn, mode=cx_Oracle.SYSDBA)

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM Guest")
            if cursor.fetchone():
                table_exists = True
    except cx_Oracle.DatabaseError:
        pass

    if not table_exists:
        print("No 'Guest' table available.")
        return

    check_out_window = tk.Toplevel()
    check_out_window.title("Check-out")
    check_out_window.geometry("300x150")
    check_out_window.configure(background="#FFDAB9")

    # Entry field for room number
    room_label = tk.Label(check_out_window, text="Room Number:")
    room_label.pack()
    room_entry = tk.Entry(check_out_window)
    room_entry.pack()

    def submit_check_out():
        # Get user input from entry field
        room_number = room_entry.get()

        try:
            # Establish a connection to the Oracle database
            dsn = cx_Oracle.makedsn("localhost", 1521, "orcl")
            connection = cx_Oracle.connect("sys", "orcl", dsn, mode=cx_Oracle.SYSDBA)

            # Check if the room number is reserved in the Stay table
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM Stay WHERE Room_Number = :1", (room_number,))
                if cursor.fetchone():
                    # Delete the reservation based on the room number from the Stay table
                    cursor.execute("DELETE FROM Stay WHERE Room_Number = :1", (room_number,))
                    connection.commit()
                    messagebox.showinfo("Check-out Successful", "Check-out successful.")
                else:
                    messagebox.showinfo("Room Not Reserved", "Room is not reserved.")

        except cx_Oracle.DatabaseError as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")

        finally:
            # Close the connection
            connection.close()

            # Close the check-out window
            check_out_window.destroy()

    # Submit button
    submit_button = tk.Button(check_out_window, text="Submit", command=submit_check_out)
    submit_button.pack(pady=(10, 0))

    # Show Reservations button
    show_reservations_button = tk.Button(check_out_window, text="Show Reservations", command=show_reservations)
    show_reservations_button.pack(pady=(10, 0))


