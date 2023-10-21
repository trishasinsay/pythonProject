import tkinter as tk
import tkinter as ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import cv2
import mysql.connector
from PIL import Image, ImageTk
from tkinter import ttk
import pytesseract
import numpy as np
from tkinter import font as tkFont
import subprocess
import re
import os
import io

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set the window's size to match the screen dimensions
        self.geometry(f"{screen_width}x{screen_height}")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MainMenu_Page, RequestPage, ValidationPage, MakerPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title('TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE')
        self.controller.iconphoto(False, tk.PhotoImage(file='tup logo 1.png'))

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill="both")

        self.canvas.config(borderwidth=0, highlightthickness=0)

        # Load the background image using PIL
        self.bg_image = Image.open('bg.png')
        self.update_background()

        # Bind the canvas to the window resizing
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.update_background()

    def update_background(self):
        # Get the screen width and height
        screen_width = self.winfo_width()
        screen_height = self.winfo_height()

        # Calculate the scaling factors for width and height
        width_scale = screen_width / self.bg_image.width
        height_scale = screen_height / self.bg_image.height

        # Resize the background image
        resized_bg_image = self.bg_image.resize((screen_width, screen_height))

        # Create a PhotoImage object from the resized image
        self.background_image = ImageTk.PhotoImage(resized_bg_image)

        # Update the canvas image
        self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)


        # Load the image
        image_path = 'logo.jpg'  # Replace with the path to your image
        if os.path.exists(image_path):
            image = Image.open(image_path)

            # Calculate the position of the image in the upper right corner
            image_width, image_height = image.size
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            image_x = screen_width - 170
            image_y = 2

            # Create a PhotoImage object from the cropped image
            image = ImageTk.PhotoImage(image)

            # Create a label to display the image with a transparent background
            image_label = tk.Label(self, image=image, bg="#666666")
            image_label.place(x=image_x, y=image_y)

            # Keep a reference to the image to prevent it from being garbage collected
            image_label.image = image
        else:
            print(f"Image file not found: {image_path}")

        # Add header text below the header rectangle
        header_text_below = self.canvas.create_text(screen_width // 2, 230, text="WELCOME", fill="white",
                                                    font=("Cambria", 110, 'bold'))

        # Add subheader text below the header text
        subheader_text = self.canvas.create_text(screen_width // 1.55, 335, text="TUPCIANS!", fill="#CF0F13",
                                                     font=('bangers', 70, 'bold'))

        # Add another text element below the subheader text
        note_text = self.canvas.create_text(screen_width // 1.45, 450,
                                            text=" Welcome! students, faculties, and Alumni, to our ID Maker Kiosk! We are thrilled to\n offer this convenient service to help you obtain your IDs. Whether you're a new or need\n a replacement ID, we're here to assist you.",
                                            fill="white",
                                            font=("roboto", 15))

        # Add clickable text button
        clickable_text = self.canvas.create_text(screen_width // 1.3, 580, text="Get Started >>", fill="white",
                                                 font=("Brush Script MT", 60))
        self.canvas.tag_bind(clickable_text, "<Button-1>", self.on_clickable_text_click)

        # Add clickable text button
        link = self.canvas.create_text(screen_width // 6 - 100, 50, text="Tupcuitc.com", fill="white",
                                       font=("Bitter", 20, 'bold', 'italic'))

        self.canvas.tag_bind(link, "<Button-1>", self.on_link_text_click)

    def on_link_text_click(self, event):
        self.on_get_started_button_click()

    def on_clickable_text_click(self, event):
        self.on_get_started_button_click()

    def on_get_started_button_click(self):
        # Switch to the main menu with three buttons
        main_menu_page_frame = MainMenu_Page(self.controller, self.controller)
        main_menu_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('MainMenu_Page')

class MainMenu_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.button_click_in_progress = False  # Initialize the flag

        # Load the background image using PIL
        self.bg_image = Image.open('mainmenu.png')  # Replace with your background image path
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a Label to display the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Bind the window resize event to update the background image
        self.bind("<Configure>", self.on_resize)

        # Create three rounded buttons
        button1 = RoundedButton(self, text="ID REQUEST FORM", command=self.on_button1_click)
        button2 = RoundedButton(self, text="ID MAKER",  command=self.on_button2_click)
        button3 = RoundedButton(self, text="ID VALIDATION", command=self.on_button3_click)
        back_button = tk.Button(self, text='BACK', font=('Cambria', 22, "bold"), command=self.on_back_button_click)

        # Use grid to place widgets
        button1.grid(row=0, column=2, sticky="nsew", padx=250, pady=80)
        button2.grid(row=1, column=2, sticky="nsew", padx=250, pady=0)
        button3.grid(row=2, column=2, sticky="nsew", padx=250, pady=60)
        back_button.grid(row=3, column=2, sticky="nsew", padx=250, pady=10)

    def on_button1_click(self):
        if self.button_click_in_progress:
            return  # Return without taking action
        self.button_click_in_progress = True

        request_page_frame = RequestPage(self.controller, self.controller)
        request_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('RequestPage')

        # Set the flag back to False when the action is complete
        self.button_click_in_progress = False

    def on_button2_click(self):
        if self.button_click_in_progress:
            return
        self.button_click_in_progress = True

        maker_page_frame = MakerPage(self.controller, self.controller)
        maker_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('MakerPage')

        self.button_click_in_progress = False

    def on_button3_click(self):
        if self.button_click_in_progress:
            return
        self.button_click_in_progress = True

        validation_page_frame = ValidationPage(self.controller, self.controller)
        validation_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('ValidationPage')

        self.button_click_in_progress = False

    def on_back_button_click(self):
        # Switch back to the StartPage
        self.controller.show_frame('StartPage')

    def on_resize(self, event):
        # Update the background image size when the window is resized
        screen_width = self.winfo_width()
        screen_height = self.winfo_height()
        resized_bg_image = self.bg_image.resize((screen_width, screen_height))
        self.bg_photo = ImageTk.PhotoImage(resized_bg_image)
        self.bg_label.configure(image=self.bg_photo)

class RoundedButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        tk.Button.__init__(self, master, **kwargs)
        self.config(relief=tk.SOLID)
        self.config(borderwidth=1)
        self.config(highlightthickness=2)
        self.config(padx=10)
        self.config(pady=10)
        self.config(bg="#2C302E")
        self.config(activebackground="white")
        self.config(foreground="white")
        self.config(font=("cambria", 22, "bold"))
        self.config(cursor="hand2")
        self.config(width=50, height=1)  # Adjust the width as needed

class ValidationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#D8D8D8')
        self.controller = controller
        self.photo = None
        self.camera_preview_initialized = False

        self.controller.title('TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE')
        self.controller.state('zoomed')
        self.controller.iconphoto(False, tk.PhotoImage(file='tup logo 1.png'))

        # Create a canvas that covers the entire frame
        self.background_image = tk.PhotoImage(file='bg.png')
        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.canvas.pack()

        # Place the background image on the canvas
        self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)


        # Create a label in front of the background image
        # Create a transparent label using a Canvas
        heading_text = 'WELCOME'
        heading_label = self.canvas.create_text(self.winfo_screenwidth() // 2, self.winfo_screenheight() // 3,
                                                text=heading_text, font=('caveat brush', 130),
                                                fill='#820505')  # Set the text color

        # Place the label in the center of the frame (adjust the values as needed)
        # Since we use canvas.create_text, there's no need for anchor=tk.CENTER
        # and we can directly set x and y coordinates.
        # Adjust the y-coordinate to change the vertical position of the text.
        # For example, self.winfo_screenheight() // 2 - 50 will move the text 50 pixels up.
        self.canvas.coords(heading_label, self.winfo_screenwidth() // 3 + 140, self.winfo_screenheight() // 3 + 60)

        sub_heading_label = 'TUPCIANS!'
        sub_heading_label = self.canvas.create_text(self.winfo_screenwidth() // 2, self.winfo_screenheight() // 3,
                                                    text=sub_heading_label, font=('inter', 40, 'bold'),
                                                    fill='black')  # Set the text color
        self.canvas.coords(sub_heading_label, self.winfo_screenwidth() // 2 + 210,
                            self.winfo_screenheight() // 3 + 160)

        # Create a variable to keep track of whether a match has been found
        self.match_found = False

        # Create a variable to control whether scanning should continue
        self.continue_scanning = True




        # Define the background color for the scan button
        scan_button_bg_color = '#5D1C1C'

        # Create Scan button with background color
        self.scan_button = tk.Button(self, text='TAP TO SCAN YOUR COR', font=('inter', 25, 'bold'), fg='white', bg=scan_button_bg_color,
                                     width=25, command=self.start_camera_and_text_detection)
        self.scan_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)  # Adjust the values of relx and rely


    def start_camera_and_text_detection(self):
        # Create a canvas to display the camera preview
        self.camera_preview_label = tk.Label(self, width=900, height=650)
        self.camera_preview_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        # Create a label for the text extraction results
        self.text_result_label = tk.Label(self, text='', font=('inter', 14), fg='white', bg='#5D1C1C')
        self.text_result_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Create a StringVar to hold the extracted text
        self.extracted_text_var = tk.StringVar()

        self.initialize_camera_preview()

    def initialize_camera_preview(self):
        if not self.camera_preview_initialized:
            try:
                # Open the camera (replace '0' with the correct camera index or device name)
                self.cap = cv2.VideoCapture(0)  # Use '1' for a secondary camera
                if not self.cap.isOpened():
                    raise Exception("Camera not opened")
                self.camera_preview_initialized = True
            except Exception as e:
                print("Camera initialization error:", str(e))

        self.update_camera_preview()

    def update_camera_preview(self):
        if self.continue_scanning:  # Check if scanning should continue and a match has not been found
            # Read a frame from the camera
            ret, frame = self.cap.read()

            if ret:
                # Enhance the color (contrast stretching)
                frame = self.enhance_color(frame)

                # Convert the frame to RGB format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                photo = ImageTk.PhotoImage(image=image)

                # Extract text and draw a bounding box
                extracted_text, bbox_image = self.extract_text_from_image(frame_rgb)
                self.text_result_label.config(text=extracted_text)

                # Convert the frame with the bounding box to PhotoImage
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(bbox_image))

                # Update the canvas with the new frame
                self.camera_preview_label.config(image=photo)
                self.camera_preview_label.image = photo

                # Check for a match in the database
                if not self.match_found:  # Check if a match has not been found
                    self.check_database_match(extracted_text)

            # Schedule the update method to be called again after 10ms
            self.after(10, self.update_camera_preview)

    def extract_text_from_image(self, image):
        # Convert the OpenCV BGR image to RGB format
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Use Tesseract to perform OCR and extract text from the image
        extracted_text = pytesseract.image_to_string(Image.fromarray(image_rgb))

        # Draw a bounding box around the detected text (resize the bounding box)
        d = pytesseract.image_to_boxes(Image.fromarray(image_rgb))
        for b in d.splitlines():
            b = b.split()
            # Resize the bounding box by multiplying the coordinates by a scaling factor
            scale_factor = 1.5  # Adjust this value to resize the bounding box as needed
            x1, y1, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            x1, y1, x2, y2 = int(x1 * scale_factor), int(y1 * scale_factor), int(x2 * scale_factor), int(y2 * scale_factor)
            image_rgb = cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 0, 255), 2)

        return extracted_text, image_rgb

    def stop_camera(self):
        # Release the camera
        if self.cap is not None:
            self.cap.release()

    def on_leave(self):
        # Call the function to close the camera when leaving the page
        self.stop_camera()

    def enhance_color(self, frame):
        # Apply contrast stretching or color enhancement here
        # Example: Increase the contrast
        min_value = np.min(frame)
        max_value = np.max(frame)
        frame = ((frame - min_value) / (max_value - min_value) * 255).astype(np.uint8)
        return frame

    def check_database_match(self, extracted_text):
        if extracted_text:
            # Replace with your database credentials
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Root030702",
                port=330,
                database="kiosk_db"
            )

            cursor = db.cursor()

            cursor.execute("SELECT Student No. FROM enrollment-list")
            results = cursor.fetchall()

            db.close()

            # Extract the ID numbers from the results and normalize them (e.g., remove spaces and convert to uppercase)
            id_numbers = {result[0].strip().upper() for result in results}

            # Normalize the extracted text for comparison
            extracted_text_normalized = extracted_text.strip().upper()

            # Use regular expressions to find and extract the format "TUPC-##-####" from the text
            match = re.search(r'TUPC-\d{2}-\d{4}', extracted_text_normalized)
            if match:
                extracted_format = match.group(0)  # Extract the matched format
                print("Extracted Format:", extracted_format)  # Cleaned and normalized extracted format

                # Define a regular expression pattern for the expected format "TUPC-##-####"
                expected_format_pattern = r'^TUPC-\d{2}-\d{4}$'

                # Check if the extracted format matches the expected format
                if re.match(expected_format_pattern, extracted_format):
                    if extracted_format in id_numbers:
                        print("Matched")
                        self.match_found = True  # Set the match_found flag to True
                        self.continue_scanning = False  # Stop scanning
                        # Show a confirmation message
                        messagebox.showinfo("Validation Successful", "Your ID is now Validated")


                        self.controller.show_frame("StartPage")

                        # Reset the camera initialization flag
                        self.initialize_camera_preview()

                        # Clear previous text and image
                        self.text_result_label.config(text='')
                        self.camera_preview_label.config(image='')

                    else:
                        print("Not Matched")
                        # Show a message box with scan again or cancel options
                        response = messagebox.askquestion("Validation Failed", "The ID is not in the database. Scan again?",
                                                          icon='warning')
                        if response == 'yes':
                            # User chose to scan again, do nothing as the camera will continue scanning
                            pass
                        else:
                            # User chose to cancel, go back to the StartPage
                            self.controller.show_frame("StartPage")
                else:
                    print("Extracted format does not match the expected format (TUPC-##-####)")

                    # Show a message box with scan again or cancel options
                    response = messagebox.askquestion("Validation Failed", "Invalid ID format. Scan again?",
                                                      icon='warning')
                    if response == 'yes':
                        # User chose to scan again, do nothing as the camera will continue scanning
                        pass
                    else:
                        # User chose to cancel, go back to the StartPage
                        self.controller.show_frame("StartPage")


            else:
                print("No valid format found in the extracted text")
                # Show a message box with scan again or cancel options
                response = messagebox.askquestion("Validation Failed", "No valid ID format found. Scan again?", icon='warning')
                if response == 'yes':
                    # User chose to scan again, do nothing as the camera will continue scanning
                    pass
                else:
                    # User chose to cancel, go back to the StartPage
                    self.controller.show_frame("StartPage")
        else:
            print("No text detected")

    def go_to_matching_page(self):
        # Reset the flags when the user returns to the ValidationPage
        self.match_found = False
        self.continue_scanning = True

        # Initialize and start scanning when entering the validation page
        self.controller.frames["ValidationPage"].initialize_camera_preview()
        self.controller.show_frame('ValidationPage')


class RequestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill="both")

        self.canvas.config(borderwidth=0, highlightthickness=0)

        # Load the background image using PIL
        self.bg_image = Image.open('req_bg.png')
        self.update_background()

        # Bind the canvas to the window resizing
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.update_background()

    def update_background(self):
        # Get the screen width and height
        screen_width = self.winfo_width()
        screen_height = self.winfo_height()

        # Calculate the scaling factors for width and height
        width_scale = screen_width / self.bg_image.width
        height_scale = screen_height / self.bg_image.height

        # Resize the background image
        resized_bg_image = self.bg_image.resize((screen_width, screen_height))

        # Create a PhotoImage object from the resized image
        self.background_image = ImageTk.PhotoImage(resized_bg_image)

        # Update the canvas image
        self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)

        # Add a header rectangle
        header_rectangle = self.canvas.create_rectangle(0, 0, screen_width, 50, fill="black")

        # Add header text inside the rectangle
        header_text = self.canvas.create_text(screen_width // 2 + 30, 25, text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE", fill="white",
                                              font=("Cambria", 20))

        # Load the image you want to display
        image_path = 'tup.jpg'  # Replace with your image file path
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image.thumbnail((90, 40))  # Adjust the size as needed
            image = ImageTk.PhotoImage(image)

            # Create a label to display the image
            image_label = tk.Label(self, image=image, bg="white", borderwidth=0, highlightthickness=0)
            image_label.photo = image
            image_label.place(x=260, y=6)  # Adjust the position as needed


        # Add header text below the header rectangle
        header_text_below = self.canvas.create_text(screen_width // 2, 90, text="REQUEST FORM", fill="white",
                                                    font=('IBMPlexMono-Bold.ttf', 25, 'bold'))

        # Add header text below the header rectangle
        notetext_below = self.canvas.create_text(screen_width // 2 + 20, 130, text="Kindly provide the complete information needed in this online form.", fill="white",
                                                    font=('IBM Plex Mono', 14))

        # Add header text below the header rectangle
        note_text_below = self.canvas.create_text(screen_width // 2 + 20, 160, text="There is a 150 pesos ID fee to be paid at the Cashier's Office for the replacement.",
                                                 fill="white", font=('IBM Plex Mono', 14))

        # Create a label for the user's role in university
        role_label = tk.Label(self, text="Role in University:", font=("Arial", 18), bg="#470000", fg='white')
        role_label.place(x=100, y=210)

        role_choices = ["Select Role", "Student", "Faculty", "Staff", "Alumni"]
        self.role_combobox = ttk.Combobox(self, values=role_choices, state='readonly', font=("Arial", 16))
        self.role_combobox.current(0)
        self.role_combobox.place(x=370, y=210, width=750, height=30)
        self.role_combobox.set("Select Role")  # Set the default value

        # Create a label for the user's email
        email_label = tk.Label(self, text="GSFE Email:", font=("Arial", 18), bg="#470000", fg='white')
        email_label.place(x=100, y=250)

        # Create an entry widget for the user's email
        self.email_entry = tk.Entry(self, font=("Arial", 16))
        self.email_entry.place(x=370, y=250, width=750, height=30)

        # Create a label for the student ID
        id_number_label = tk.Label(self, text="Student ID:", font=("Arial", 18), bg="#470000", fg='white')
        id_number_label.place(x=100, y=290)

        # Create an entry widget for the student ID
        self.id_number_entry = tk.Entry(self, font=("Arial", 16))
        self.id_number_entry.place(x=370, y=290,  width=750, height=30)

        # Create a label for the student request
        request_type_label = tk.Label(self, text="Type of ID Request:", font=("Arial", 18), bg="#470000", fg='white')
        request_type_label.place(x=100, y=330)

        request_choices = ["Type of ID Request", "REPLACEMENT (for old students with lost ID)", "REPLACEMENT (for old students with damaged ID that needs replacement)", "UNCLAIMED", "Alumni"]
        self.request_combobox = ttk.Combobox(self, values=request_choices, state='readonly', font=("Arial", 16))
        self.request_combobox.current(0)
        self.request_combobox.place(x=370, y=330, width=750, height=30)
        self.request_combobox.set("Select Type of Request")  # Set the default value

        # Create a label for the reason
        reason_label = tk.Label(self, text="Reason:", font=("Arial", 18), bg="#470000",
                                      fg='white')
        reason_label.place(x=100, y=370)

        self.reason_entry = tk.Entry(self, font=("Arial", 16))
        self.reason_entry.place(x=370, y=370, width=750, height=30)

        # Create a label for the student lastname
        lastname_label = tk.Label(self, text="Last Name:", font=("Arial", 18), bg="#470000", fg='white')
        lastname_label.place(x=100, y=410)

        # Create an entry widget for the student lastname
        self.lastname_entry = tk.Entry(self, font=("Arial", 16))
        self.lastname_entry.place(x=370, y=410,  width=750, height=30)

        # Create a label for the student firstname
        firstname_label = tk.Label(self, text="First Name:", font=("Arial", 18), bg="#470000", fg='white')
        firstname_label.place(x=100, y=450)

        # Create an entry widget for the student firstname
        self.firstname_entry = tk.Entry(self, font=("Arial", 16))
        self.firstname_entry.place(x=370, y=450, width=750, height=30)

        # Create a label for the student middle name
        middlename_label = tk.Label(self, text="Middle Name:", font=("Arial", 18), bg="#470000", fg='white')
        middlename_label.place(x=100, y=490)

        # Create an entry widget for the student middle name
        self.middlename_entry = tk.Entry(self, font=("Arial", 16))
        self.middlename_entry.place(x=370, y=490,  width=750, height=30)

        # Create a label for the student contact number
        contact_label = tk.Label(self, text="Contact No.:", font=("Arial", 18), bg="#470000", fg='white')
        contact_label.place(x=100, y=530)

        # Create an entry widget for the student contact number
        self.contact_entry = tk.Entry(self, font=("Arial", 16))
        self.contact_entry.place(x=370, y=530,  width=750, height=30)

        # Create a label for the student program or course
        program_label = tk.Label(self, text="Program:", font=("Arial", 18), bg="#470000", fg='white')
        program_label.place(x=100, y=570)

        program_choices =["Program",
                             "BSCE", "BSEE", 'BSME', 'BSIE-ICT', "BSIE-HE", "BSIE-IA", "BTTE-CP",
                             "BTTE-EI", "BTTE-AU", "BTTE-HVACT", "BTTE-E", "BGT-AT", "BET-CT",
                             "BET-ET", "BET-ESET", "BET-COET", "BET-MT", "BET-PPT", "BET-AT"
                        ]
        self.program_combobox = ttk.Combobox(self, values=program_choices, state='readonly', font=('Arial', 16))
        self.program_combobox.current(0)
        self.program_combobox.place(x=370, y=570,  width=750, height=30)
        self.program_combobox.set("Select your Program")  # Set the default value

        # Create the "Clear" button
        clear_button = tk.Button(self, text="Clear", font=("IBM Plex Mono", 14, 'bold'), command=self.clear_form,
                                  width=12)
        clear_button.place(relx=0.06, rely=0.95, anchor="sw")

        # Create the "Submit" button
        submit_button = tk.Button(self, text="Submit", font=("IBM Plex Mono", 14, 'bold'), command=self.submit_form, width=12)
        submit_button.place(relx=0.83, rely=0.95, anchor="se")

        # Create the "Cancel" button
        cancel_button = tk.Button(self, text="Cancel", font=("IBM Plex Mono", 14, 'bold'), command=self.cancel_form, width=12)
        cancel_button.place(relx=0.96, rely=0.95, anchor="se")

        # ... Continue with the rest of your code ...

    def submit_form(self):
        role = self.role_combobox.get()
        email = self.email_entry.get()
        id_number = self.id_number_entry.get()
        request = self.request_combobox.get()
        reason = self.reason_entry.get()
        lastname = self.lastname_entry.get()
        firstname = self.firstname_entry.get()
        middlename = self.middlename_entry.get()
        contact = self.contact_entry.get()
        program = self.program_combobox.get()

        # Create a list of all entry widgets
        entry_widgets = [
            self.email_entry, self.id_number_entry, self.reason_entry,
            self.lastname_entry, self.firstname_entry, self.middlename_entry,
            self.contact_entry
        ]

        # Create a list of corresponding dropdowns
        dropdowns = [
            self.role_combobox, self.request_combobox, self.program_combobox
        ]

        # Initialize a flag to check if any field is empty
        any_empty = False

        # Check each entry widget for empty fields
        for entry_widget in entry_widgets:
            if not entry_widget.get():
                entry_widget.config(highlightbackground="red")
                any_empty = True
            else:
                entry_widget.config(highlightbackground=None)

        # Check each dropdown for default values
        for dropdown in dropdowns:
            if dropdown.get() == dropdown["values"][0]:
                dropdown.set("")  # Clear the default value
                dropdown.configure(state="readonly")
                any_empty = True
            else:
                dropdown.config(highlightbackground=None)

        if any_empty:
            # Show an error message and return
            self.message_L.config(text="Please fill in all the required fields", fg='red')
            return

        # Construct the confirmation message
        confirmation_message = (
            f"Role: {role}\nEmail: {email}\nStudent No.: {id_number}\nType of Request: {request}\nReason: {reason}\nLast Name: {lastname}"
            f"\nFirst Name: {firstname}\nMiddle Name: {middlename}\nContact No.: {contact}\nProgram: {program}\n\nAre all the information provided is correct?"
        )

        # Display a confirmation message box
        user_response = messagebox.askquestion("Confirmation", confirmation_message)

        if user_response == 'yes':
            # User clicked "OK," so save the data to the database
            if self.save_to_database(email, id_number, role):
                messagebox.showinfo("Success", "Data saved successfully.")
            else:
                messagebox.showerror("Error", "Failed to save data to the database.")
        else:
            # User clicked "Cancel"
            messagebox.showinfo("Cancelled", "Data not saved")

    def validate_email(self):
        # Get the email from the entry field
        email = self.email_entry.get()

        if not email:
            # The email field is empty, so show an error message and change the border color
            self.email_entry.config(highlightbackground="red")
        else:
            # The email field is filled, so reset the border color to the default
            self.email_entry.config(highlightbackground=None)

    def save_to_database(self, email, id_number, role):
        try:
            # Replace with your database credentials
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Root030702",
                database="kiosk_db"
            )

            cursor = db.cursor()

            # Replace with your database table and column names
            query = "INSERT INTO tbl_request (Role, Email, StudentID, Request, Reason, LastName, FirstName, MiddleName, ContactNo, Program) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,  %s)"
            values = (self.role_combobox, self.email_entry, self.id_number_entry, self.request_combobox, self.reason_entry, self.lastname_entry, self.firstname_entry, self.middlename_entry, self.contact_entry, self.program_combobox)

            cursor.execute(query, values)
            db.commit()
            db.close()
            return True
        except Exception as e:
            print("Database error:", str(e))
            return False

        self.role_combobox.set('')
        self.role_combobox.current(0)

        self.email_entry.delete(0, 'end')  # Clear the email Entry widget
        self.id_number_entry.delete(0, 'end')  # Clear the id_number Entry widget

        self.request_combobox.set('')
        self.request_combobox.current(0)

        self.reason_entry.delete(0, 'end')  # Clear the reason Entry widget
        self.lastname_entry.delete(0, 'end')  # Clear the lastname Entry widget
        self.firstname_entry.delete(0, 'end')  # Clear the firstname Entry widget
        self.middlename_entry.delete(0, 'end')  # Clear the middlename Entry widget
        self.contact_entry.delete(0, 'end')  # Clear the contact Entry widget

        self.program_combobox.set('')
        self.program_combobox.current(0)

    def cancel_form(self):
        self.controller.show_frame("StartPage")

    def clear_form(self):
        self.role_combobox.set('')
        self.role_combobox.current(0)

        self.email_entry.delete(0, 'end')  # Clear the email Entry widget
        self.id_number_entry.delete(0, 'end')  # Clear the id_number Entry widget

        self.request_combobox.set('')
        self.request_combobox.current(0)

        self.reason_entry.delete(0, 'end')  # Clear the reason Entry widget
        self.lastname_entry.delete(0, 'end')  # Clear the lastname Entry widget
        self.firstname_entry.delete(0, 'end')  # Clear the firstname Entry widget
        self.middlename_entry.delete(0, 'end')  # Clear the middlename Entry widget
        self.contact_entry.delete(0, 'end')  # Clear the contact Entry widget

        self.program_combobox.set('')
        self.program_combobox.current(0)


class MakerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#5D1C1C')
        self.controller = controller

        # Create a canvas that covers the entire frame
        self.background_image = tk.PhotoImage(file='bg.png')
        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.canvas.pack()

        # Place the background image on the canvas
        self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)

        heading_text = 'TUPC KIOSK ID MAKER'
        heading_label = self.canvas.create_text(self.winfo_screenwidth() // 2, self.winfo_screenheight() // 3,
                                                text=heading_text, font=('caveat brush', 70),
                                                fill='#820505')  # Set the text color

        # Place the label in the center of the frame (adjust the values as needed)
        # Since we use canvas.create_text, there's no need for anchor=tk.CENTER
        # and we can directly set x and y coordinates.
        # Adjust the y-coordinate to change the vertical position of the text.
        # For example, self.winfo_screenheight() // 2 - 50 will move the text 50 pixels up.
        self.canvas.coords(heading_label, self.winfo_screenwidth() // 3 + 220, 110)

        sub_heading_label = 'Enter your Student ID Number'
        sub_heading_label = self.canvas.create_text(self.winfo_screenwidth() // 2, self.winfo_screenheight() // 3,
                                                    text=sub_heading_label, font=('cambria', 35, 'bold'),
                                                    fill='black')  # Set the text color
        self.canvas.coords(sub_heading_label, self.winfo_screenwidth() // 2 , 260)

        # Create an Entry widget for the Student ID
        self.id_entry = tk.Entry(self, font=('cambria', 25, 'bold'), width=40, justify='center', bg='#D8D8D8')
        self.canvas.create_window(self.winfo_screenwidth() // 2, 350,
                                  window=self.id_entry)


        #note_label = tk.Label(self, text="*Note: Enter your Student ID", font=('inter', 12), fg='gray')
        #self.canvas.create_window(self.winfo_screenwidth() // 2, self.winfo_screenheight() // 2 + 260,
                                  #window=note_label)

        # Create the "Get Started" button
        submit_button = tk.Button(self, text='SUBMIT', font=('inter', 20, 'bold'),
                                       command=self.on_get_started_button_click, bg='#5D1C1C', fg='white',
                                       width=15, height=1)

        # Place the button below the sub-heading label
        self.canvas.create_window(self.winfo_screenwidth() // 2 + 10, self.winfo_screenheight() // 2 + 190,
                                  window=submit_button)

    def on_get_started_button_click(self):
        # Create a label for displaying the error message
        self.invalid_label = tk.Label(self, text="", fg="red")
        self.invalid_label.pack()

        # Retrieve the Student ID from the Entry widget
        student_id = self.id_entry.get()
        faculty_id = self.id_entry.get()

        # Define a regular expression pattern to match the desired format
        pattern1 = r'^TUPC-\d{2}-\d{4}$'
        pattern2 = r'^TUPC-ID NO.\d{4}$'

        # Check if the entered text matches the pattern
        if re.match(pattern1, student_id):
            subprocess.Popen(['python', 'id_front.py'])
            self.id_entry.delete(0, tk.END)
        elif re.match(pattern2, faculty_id):
            subprocess.Popen(['python', 'faculty.py'])
            self.id_entry.delete(0, tk.END)
        else:
            # If the format is incorrect, show an error message or take other actions as needed
            if self.id_entry.get() != student_id and faculty_id:
                self.invalid_label.config(text="INVALID FORMAT")


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()