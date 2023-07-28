import tkinter as tk
from tkinter import PhotoImage, filedialog
from tkinter import messagebox
from PIL import Image, ImageTk  # Importing the necessary modules from Pillow
import cv2
import numpy as np
import os
import pytesseract

class MyProgram:
    root = None
    file_path = ''
    tesseract_file_path = ''
    canvas = None
    image = None
    manipulated_image = None

    def __init__(self, config):
        self.program_name = config.get("General", "ProgramName")
        
        # setting the pytesseract path
        self.choose_tesseract_exe()

        
        # Initialize the GUI
        self.init_gui()



    def init_gui(self): # TODO the check box for gray scale for some reason still showing as a slider
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
        self.root = tk.Tk()
        self.root.title(self.program_name)

        # Set the minimum size of the window (600x500 pixels)
        self.root.minsize(650, 500)

        # Set the initial size of the window
        self.root.geometry("600x500")

        # Create a label to display the program name
        label = tk.Label(self.root, text=self.program_name, font=("Helvetica", 20))
        label.pack(pady=10)

        # Create the canvas for the rectangular image
        self.rectangle = tk.Canvas(self.root, width=300, height=200)
        self.rectangle.pack(pady=5)

        # Draw an empty rectangular image on the canvas
        self.rectangle.create_rectangle(10, 10, 290, 190, outline="black", fill="white")


        # Create buttons to select an image & extract text
        buttons_frame = tk.Frame(self.root, width=250)
        buttons_frame.pack(pady=0)

        select_button = tk.Button(buttons_frame, text="Select Image", command=self.select_image)
        select_button.grid(row=0, column=0, padx=0)
        extract_button = tk.Button(buttons_frame, text="Extract Text", command=self.extract_text)
        extract_button.grid(row=0, column=1, padx=0)

        # Create manipulators for image manipulations
        self.manipulators = {}
        manipulators_names = {
            "grayscale": "Grayscale",
            "smoothing": "Smoothing",
            "threshold": "Threshold",
            "rotation": "Rotation"
        }

        for manipulation, name in manipulators_names.items():
                manipulators_frame = tk.Frame(self.root, width=250)
                manipulators_frame.pack(pady=0)

                label = tk.Label(manipulators_frame, text=name)
                label.grid(row=0, column=0, sticky=tk.W, padx=0)

                if name == "Rotation":
                    slider = tk.Scale(manipulators_frame, from_=-180, to=180, orient=tk.HORIZONTAL, length=150, command=self.apply_manipulations)
                    slider.set(0)
                    # slider.pack(side=tk.RIGHT)
                    slider.grid(row=0, column=1, padx=5)
                    self.manipulators[manipulation] = slider

                else:
                    slider = tk.Scale(manipulators_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=150, command=self.apply_manipulations)
                    slider.set(0)
                    # slider.pack(side=tk.RIGHT)
                    slider.grid(row=0, column=1, padx=5)
                    self.manipulators[manipulation] = slider

        # Run the Tkinter main loop
        self.root.mainloop()

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

    def choose_tesseract_exe(self):
        self.tesseract_file_path = filedialog.askopenfilename(title="Select tesseract.exe", filetypes=[("Executable files", "*.exe;")])
        if "tesseract.exe" not in  self.tesseract_file_path:
            messagebox.showerror("Error", "Please install tesseract-ocr first.")
            return
        else:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_file_path
        
    def load_image(self, file_path):

        # Reset the sliders
        self.reset_sliders()

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
            self.image.x = (300 - self.image.width) // 2
            self.image.y = (200 - self.image.height) // 2

            # Display the image on the canvas using ImageTk
            self.photo_image = ImageTk.PhotoImage(self.image)
            self.display_image_on_canvas(self.photo_image)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def display_image_on_canvas(self, photo_image: PhotoImage):
        # Clear the canvas first
        self.rectangle.delete("all")
        self.rectangle.create_image(self.image.x, self.image.y, anchor=tk.NW, image=photo_image)

    def apply_manipulations(self, _=None):
        # Get the slider values
        grayscale_value = int(self.manipulators["grayscale"].get()) # TODO
        smoothing_value = int(self.manipulators["smoothing"].get())
        threshold_value = float(self.manipulators["threshold"].get())
        rotation_value = int(self.manipulators["rotation"].get())

        # Update the displayed image
        if self.image is not None:
            try:
                # Make a copy of the original Pillow image to apply manipulations
                self.manipulated_image = self.image.copy()

                # Convert the Pillow image to a numpy array for OpenCV manipulations
                np_image = np.array(self.manipulated_image)

                # Apply manipulations to the image based on the slider values

                # Grayscale conversion
                if grayscale_value > 0:
                    np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
                    np_image = cv2.merge((np_image, np_image, np_image)) # making 3 channels

                # Smoothing (blur)
                if smoothing_value > 0:
                    kernel_size = (smoothing_value * 2 + 1, smoothing_value * 2 + 1)
                    np_image = cv2.GaussianBlur(np_image, kernel_size, 0)

                # Thresholding
                if grayscale_value and threshold_value > 0:
                    _, np_image = cv2.threshold(np_image, threshold_value, 255, cv2.THRESH_BINARY)

                # Rotation
                if rotation_value != 0:
                    image_center = tuple((np.array(np_image.shape[1::-1]) - 1) / 2)
                    rotation_matrix = cv2.getRotationMatrix2D(image_center, rotation_value, 1.0)
                    np_image = cv2.warpAffine(np_image, rotation_matrix, np_image.shape[1::-1], flags=cv2.INTER_LINEAR)

                # Convert the numpy array back to a Pillow Image
                self.manipulated_image = Image.fromarray(np_image)

                self.photo_image = ImageTk.PhotoImage(self.manipulated_image)
                self.display_image_on_canvas(self.photo_image)
            except Exception as e:
                self.reset_image()
                self.reset_sliders()
                print(e)
                messagebox.showerror("Error", f"Failed to apply manipulations: {e}")

    def reset_image(self):
        self.load_image(self.file_path)

    def reset_sliders(self):
        # enable all sliders and reset them
        for slider in self.manipulators.values():
            slider.set(0)

    def extract_text(self):
        if self.manipulated_image is not None:
            try:
                mytext = pytesseract.image_to_string(self.manipulated_image) 
                messagebox.showinfo("Extracted Text", f"{mytext}")
            except Exception as e:
                print(e)
                messagebox.showerror("Error", f"Failed to extract text")