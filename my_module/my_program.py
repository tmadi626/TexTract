import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk  # Importing the necessary modules from Pillow
import os

class MyProgram:
    file_path = ''
    canvas = None
    image = None

    def __init__(self, config):
        self.program_name = config.get("General", "ProgramName")
        # param1 = config.get("General", "Parameter1")
        # param2 = config.get("General", "Parameter2")
        
        # Initialize the GUI
        self.init_gui()



    def init_gui(self):
        """
        Initializes the graphical user interface (GUI) for the program.
        This function creates a Tkinter window and sets its title to the program name. The initial size of the window is set to 600x500 pixels.
        The function also creates a label to display the program name with a font size of 20. It creates a canvas with dimensions of 300x200 pixels, and draws an empty rectangular image on the canvas.
        Additionally, it creates a button labeled "Select Image" that calls the `select_image` method when clicked.
        Finally, the function starts the Tkinter main loop, which continuously runs the GUI and handles user events.

        Parameters:
        - self: The instance of the class.

        Return:
        - None
        """
        root = tk.Tk()
        root.title(self.program_name)
        # Set the minimum size of the window (600x500 pixels)
        root.minsize(600, 500)

        # Set the initial size of the window
        root.geometry("600x500")

        # Create a label to display the program name
        label = tk.Label(root, text=self.program_name, font=("Helvetica", 20))
        label.pack(pady=20)

        # Create the canvas for the rectangular image
        self.canvas = tk.Canvas(root, width=300, height=200)
        self.canvas.pack(pady=10)

        # Draw an empty rectangular image on the canvas
        self.canvas.create_rectangle(10, 10, 290, 190, outline="black", fill="white")


        # Create a button to select an image
        select_button = tk.Button(root, text="Select Image", command=self.select_image)
        select_button.pack(pady=10)

        # Run the Tkinter main loop
        root.mainloop()

    def select_image(self):
        """
        Prompts the user to select an image file and performs validation on the selected file.

        Returns:
            None
        """
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            _, file_extension = os.path.splitext(file_path)
            allowed_extensions = ['.jpg', '.jpeg', '.png']

            if file_extension.lower() in allowed_extensions:
                # print("Selected image:", file_path)
                # Load the image using Pillow
                self.load_image(file_path)

            else:
                messagebox.showerror("Invalid File", "The selected file is not a valid image.")

    def load_image(self, file_path):
        # Clear the canvas first
        self.canvas.delete("all")

        try:
            # Open the image using Pillow
            self.image = Image.open(file_path)

            # Get the size of the image
            image_width, image_height = self.image.size

            # Resize the image if needed to fit within the canvas
            max_width = 280
            max_height = 180
            if image_width > max_width or image_height > max_height:
                self.image.thumbnail((max_width, max_height))

            # Calculate the position to center the image on the canvas
            x = (300 - self.image.width) // 2
            y = (200 - self.image.height) // 2

            # Display the image on the canvas using ImageTk
            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo_image)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")


    def run(self):
        print(f"Running {self.program_name}")