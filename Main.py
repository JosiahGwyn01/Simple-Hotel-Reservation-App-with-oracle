import tkinter as tk
from PIL import ImageTk,Image
import check_in
import check_out
import show_current_reservations
import cx_Oracle

def apply_opacity(image_path, opacity):
    original_image = Image.open(image_path).convert("RGBA")
    width, height = original_image.size

    transparent_image = Image.new("RGBA", (width, height))
    for x in range(width):
        for y in range(height):
            r, g, b, a = original_image.getpixel((x, y))
            transparent_image.putpixel((x, y), (r, g, b, int(a * opacity)))

    return transparent_image

def main_menu():
    root = tk.Tk()
    root.title("Hotel Reservation App")
    root.geometry("1200x800")

    # Load the image
    image_path = "D:\CODING\Hotel_Reservation\wallpaper2.jpg"
    opacity = 1.0  # Set the desired opacity (0.0 - 1.0)
    image = apply_opacity(image_path, opacity)
    image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))  # Resize the image to fit the window

    # Create a PhotoImage object from the image
    background_image = ImageTk.PhotoImage(image)

    # Create a Label widget to display the image
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Style for the buttons
    button_style = {
        'font': ('Tahoma', 16),
        'width': 25,
        'height': 4,
        'bg': '#FFE5B4',
        'fg': 'black',
        'relief': 'raised'
    }

    text_label = tk.Label(root, text="Welcome to Hotel Reservation App", font=('Tahoma', 36, 'bold'), bg='#FFE5B4', relief='solid', borderwidth=6, pady=10)
    text_label.pack(pady=20)

    def open_check_in():
        check_in.enter_details()

    def open_check_out():
        check_out.check_out()

    def show_reservations():
        show_current_reservations.show_current_reservations()

    check_in_button = tk.Button(root, text="Check-in", command=open_check_in, **button_style)
    check_in_button.pack(pady=10)

    check_out_button = tk.Button(root, text="Check-out", command=open_check_out, **button_style)
    check_out_button.pack(pady=10)

    show_reservations_button = tk.Button(root, text="Show Current Reservations", command=show_reservations, **button_style)
    show_reservations_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.destroy, **button_style)
    exit_button.pack(pady=20)

    root.mainloop()




# Run the main menu
if __name__ == "__main__":
    main_menu()
