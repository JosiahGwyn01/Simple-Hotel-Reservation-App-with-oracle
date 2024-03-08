import tkinter as tk
import cx_Oracle
from tkinter import messagebox
from tkinter import ttk

def show_current_reservations():
    try:
        # Establish a connection to the Oracle database
        dsn = cx_Oracle.makedsn("localhost", 1521, "orcl")
        connection = cx_Oracle.connect("sys", "orcl", dsn, mode=cx_Oracle.SYSDBA)

        # Check if the "Guests" and "Room_Type" tables exist
        guest_table_exists = False
        room_table_exists = False
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM Guest")
            if cursor.fetchone():
                guest_table_exists = True

            cursor.execute("SELECT 1 FROM Room")
            if cursor.fetchone():
                room_table_exists = True

        if guest_table_exists and room_table_exists:
            # Fetch relevant columns from the Guests table
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT g.Name, r.Room_Type, r.Room_Number, s.Fees
                    FROM Stay s
                    INNER JOIN Guest g ON s.Guest_ID = g.Guest_ID
                    INNER JOIN Room r ON s.Room_Number = r.Room_Number
                    ORDER BY g.Name, r.Room_Type, r.Room_Number, s.Fees
                    """
                )
                rows = cursor.fetchall()

            # Create a Tkinter window for displaying the table
            root = tk.Tk()
            root.title("Current Reservations")

            # Create a treeview widget
            tree = ttk.Treeview(root)
            tree["columns"] = ("name", "room_type", "room_number", "fees")
            tree.column("#0", width=1)  # To remove the dead space

            tree.column("name", width=100)
            tree.column("room_type", width=100)
            tree.column("room_number", width=100)
            tree.column("fees", width=100)

            tree.heading("#0", text="")
            tree.heading("name", text="Name")
            tree.heading("room_type", text="Room Type")
            tree.heading("room_number", text="Room Number")
            tree.heading("fees", text="Fees")  

            for row in rows:
                name, room_type, room_number, fees = row  
                tree.insert("", tk.END, values=(name, room_type, room_number, fees))  

            tree.pack(fill="both", expand=True)  # Fill the available space

            root.mainloop()
        else:
            messagebox.showerror("Error", "Required tables do not exist.")

    except cx_Oracle.DatabaseError as error:
        messagebox.showerror("Error", f"An error occurred: {error}")

    # Close the connection
    connection.close()


# Run the show_current_reservations function
if __name__ == "__main__":
    show_current_reservations()
