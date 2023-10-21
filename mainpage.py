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
    # Define screen_width and screen_height as class attributes
    screen_width = 0
    screen_height = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Set initial screen width and height
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Create a Canvas to display the background image
        self.canvas = tk.Canvas(self, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()

        # Load the background image using PIL
        self.bg_image = Image.open('bg.png')  # Replace with your background image path
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a Label to display the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Bind the window resize event to update the background image
        self.bind("<Configure>", self.on_resize)

        # Load the image
        image_path = 'logo.jpg'  # Replace with the path to your image
        if os.path.exists(image_path):
            image = Image.open(image_path)

            # Calculate the position of the image in the upper right corner
            image_width, image_height = image.size
            image_x = self.screen_width - 160  # Access screen_width as a class attribute
            image_y = 0

            # Create a PhotoImage object from the cropped image
            image = ImageTk.PhotoImage(image)

            # Create a background rectangle with color #666666
            bg_rect = tk.Label(self, bg="#666666")
            bg_rect.place(x=image_x, y=image_y, width=image_width, height=image_height)

            # Create a label to display the image with a transparent background
            image_label = tk.Label(self, image=image, bg="#666666")
            image_label.place(x=image_x, y=image_y)

            # Keep a reference to the image to prevent it from being garbage collected
            image_label.image = image
        else:
            print(f"Image file not found: {image_path}")

        # Add header text below the header rectangle
        header_text_below = self.canvas.create_text(self.screen_width // 2, 230, text="WELCOME", fill="white",
                                                    font=("Cambria", 110, 'bold'))

        # Add subheader text below the header text
        subheader_text = self.canvas.create_text(self.screen_width // 1.55, 335, text="TUPCIANS!", fill="#CF0F13",
                                                 font=('bangers', 70, 'bold'))

        # Add another text element below the subheader text
        note_text = self.canvas.create_text(self.screen_width // 1.45, 450,
                                            text=" Welcome! students, faculties, and Alumni, to our ID Maker Kiosk! We are thrilled to\n offer this convenient service to help you obtain your IDs. Whether you're a new or need\n a replacement ID, we're here to assist you.",
                                            fill="white",
                                            font=("roboto", 15))

        # Add clickable text button
        clickable_text = self.canvas.create_text(self.screen_width // 1.3, 580, text="Get Started >>", fill="white",
                                                 font=("Brush Script MT", 60))
        self.canvas.tag_bind(clickable_text, "<Button-1>", self.on_clickable_text_click)

        # Add clickable text button
        link = self.canvas.create_text(self.screen_width // 6 - 100, 50, text="Tupcuitc.com", fill="white",
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

    def on_resize(self, event):
        # Update the background image size when the window is resized
        screen_width = event.width
        screen_height = event.height
        resized_bg_image = self.bg_image.resize((screen_width, screen_height))
        self.bg_photo = ImageTk.PhotoImage(resized_bg_image)
        self.bg_label.configure(image=self.bg_photo)


class MainMenu_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Load the background image using PIL
        self.bg_image = Image.open('mainmenu.png')  # Replace with your background image path
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a Label to display the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Bind the window resize event to update the background image
        self.bind("<Configure>", self.on_resize)

        # Create the content for the new frame
        new_frame_label = tk.Label(self, text='This is the New Frame', font=('inter', 24, 'bold'))
        new_frame_label.pack(pady=20, padx=20)

        # Add other widgets and content as needed
        # ...

        # Create a button to go back to the StartPage
        back_button = tk.Button(self, text='Back to Start Page', font=('inter', 16),
                                command=self.on_back_button_click)
        back_button.pack(pady=10)

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
                self.cap = cv2.VideoCapture(1)  # Use '1' for a secondary camera
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
        tk.Frame.__init__(self, parent, bg='#EFEFEF')  # Set the background color for the entire page
        self.controller = controller

        # Create a colored square background frame to hold the labels and input fields
        form_frame = tk.Frame(self, bg='#5D1C1C', padx=50, pady=50)
        form_frame.pack(expand=True, fill=tk.BOTH)  # Allow the form_frame to fill available space

        # Create a label for the RegistrationPage
        request_label = tk.Label(form_frame, text="REQUEST FORM", font=('inter', 30, 'bold'), bg='#5D1C1C',
                                 fg='#FFFFFF')
        request_label.grid(row=0, column=0, columnspan=3, padx=450, pady=18, sticky='NW')

        note_label = tk.Label(form_frame,
                              text="Kindly provide the complete information needed in this online form.\n\n"
                                   "There is a 150 pesos ID fee to be paid at the Cashier's Office for the replacement.",
                              font=('inter', 15), bg='#5D1C1C', fg='#FFFFFF')
        note_label.grid(row=2, column=1, padx=70, pady=30, sticky='w')

        id_label = tk.Label(form_frame, text='ID Number:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        id_label.grid(row=4, column=0, padx=10, pady=15, sticky='e')

        self.id_var = tk.StringVar()
        self.id_entry = tk.Entry(form_frame, font=('inter', 14), width=25, textvariable=self.id_var)
        self.id_entry.grid(row=4, column=1, padx=10, pady=15, sticky='w')

        FirstName_label = tk.Label(form_frame, text='Last Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        FirstName_label.grid(row=5, column=0, padx=10, pady=15, sticky='e')

        self.FirstName_var = tk.StringVar()
        self.FirstName_entry = tk.Entry(form_frame, font=('inter', 14), width=25, textvariable=self.FirstName_var)
        self.FirstName_entry.grid(row=5, column=1, padx=10, pady=15, sticky='w')

        MiddleName_label = tk.Label(form_frame, text='First Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        MiddleName_label.grid(row=6, column=0, padx=10, pady=15, sticky='e')

        self.MiddleName_var = tk.StringVar()
        self.MiddleName_entry = tk.Entry(form_frame, font=('inter', 14), width=25, textvariable=self.MiddleName_var)
        self.MiddleName_entry.grid(row=6, column=1, padx=10, pady=15, sticky='w')

        LastName_label = tk.Label(form_frame, text='Middle Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        LastName_label.grid(row=7, column=0, padx=10, pady=15, sticky='e')

        self.LastName_var = tk.StringVar()
        self.LastName_entry = tk.Entry(form_frame, font=('inter', 14), width=25, textvariable=self.LastName_var)
        self.LastName_entry.grid(row=7, column=1, padx=10, pady=15, sticky='w')

        course_label = tk.Label(form_frame, text='Course:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        course_label.grid(row=8, column=0, padx=10, pady=15, sticky='e')

        self.course_var = tk.StringVar()
        course_combobox = ttk.Combobox(form_frame, textvariable=self.course_var,
                                       values=["Bachelor of Science in Civil Engineering (BSCE)",
                                               "Bachelor of Science in Electrical Engineering (BSEE)",
                                               "Bachelor of Science in Mechanical Engineering (BSME)",
                                               "Bachelor of Science in Industrial Education major in Information and Communications Technology (BSIE-ICT)",
                                               "Bachelor of Science in Industrial Education major in Home Economics (BSIE-HE)",
                                               "Bachelor of Science in Industrial Education major in Industrial Arts (BSIE-IA)",
                                               "Bachelor of Technical Vocational Teacher Education major in Computer Programming (BTTE-CP)",
                                               "Bachelor of Technical Vocational Teacher Education major in Electrical (BTTE-EI)",
                                               "Bachelor of Technical Vocational Teacher Education major in Automotive (BTTE-Au)",
                                               "Bachelor of Technical Vocational Teacher Education major in Heating, Ventilation and Airconditioning Technology (BTTE-HVACT)",
                                               "Bachelor of Technical Vocational Teacher Education major in Electronics (BTTE-E)",
                                               "Bachelor of Graphics Technology in Architecture (BGT-AT)",
                                               "Bachelor of Engineering Technology major in Civil Technology (BET-CT)",
                                               "Bachelor of Engineering Technology major in Electrical Technology (BET-ET)",
                                               "Bachelor of Engineering Technology major in Electronics Technology (BET-EsET)",
                                               "Bachelor of Engineering Technology major in Computer Engineering Technology (BET-CoET)",
                                               "Bachelor of Engineering Technology major in Mechanical Technology (BET-MT)",
                                               "Bachelor of Engineering Technology major in Powerplant Technology (BET-PPT)",
                                               "Bachelor of Engineering Technology major in Automotive Technology (BET-AT)"],
                                       font=('inter', 12), state="readonly", width=110)
        course_combobox.grid(row=8, column=1, padx=10, pady=15, sticky="w")

        request_type_label = tk.Label(form_frame, text='Type of Request:', font=('inter', 18), bg='#5D1C1C',
                                      fg='#FFFFFF')
        request_type_label.grid(row=4, column=1, padx=450, pady=15, sticky='e')

        self.type_var = tk.StringVar()
        request_type_combobox = ttk.Combobox(form_frame, textvariable=self.type_var,
                                             values=["REPLACEMENT(For old students with lost ID",
                                                     "REPLACEMENT(For old students with damaged ID that needs replacement",
                                                     "New ID"],
                                             font=('inter', 12), state="readonly", width=45)
        request_type_combobox.grid(row=4, column=1, padx=20, pady=15, sticky="e")

        role_label = tk.Label(form_frame, text='Role in University:', font=('inter', 18), bg='#5D1C1C',
                              fg='#FFFFFF')
        role_label.grid(row=5, column=1, padx=440, pady=15, sticky='e')

        self.role_var = tk.StringVar()
        role_combobox = ttk.Combobox(form_frame, textvariable=self.role_var,
                                     values=["Student", "Faculty", "Alumni"],
                                     font=('inter', 12), state="readonly", width=25)
        role_combobox.grid(row=5, column=1, padx=190, pady=15, sticky="e")

        # Create the Proceed button, but set it to be disabled initially
        self.submit_button = tk.Button(form_frame, text='Submit', font=('inter', 18), command=self.show_confirmation,
                                       bg='#5D1C1C', fg='#FFFFFF', width=8, state=tk.DISABLED)
        self.submit_button.grid(row=9, column=1, rowspan=10, padx=35, pady=5, sticky='se')

        # Create the cancel button
        clear_button = tk.Button(form_frame, text='Clear', font=('inter', 18), command=self.clear_form,
                                  bg='#5D1C1C', fg='#FFFFFF', width=8)
        clear_button.grid(row=9, column=1, rowspan=10, padx=10, pady=5, sticky='s')

        # Create the cancel button
        cancel_button = tk.Button(form_frame, text='Cancel', font=('inter', 18), command=self.cancel_form,
                                  bg='#5D1C1C', fg='#FFFFFF', width=8)
        cancel_button.grid(row=9, column=0, rowspan=10, padx=35, pady=5, sticky='sw')

        # Bind the validation function to the variables
        self.id_var.trace_add("write", self.validate_fields)
        self.FirstName_var.trace_add("write", self.validate_fields)
        self.MiddleName_var.trace_add("write", self.validate_fields)
        self.LastName_var.trace_add("write", self.validate_fields)
        self.course_var.trace_add("write", self.validate_fields)
        self.type_var.trace_add("write", self.validate_fields)
        self.role_var.trace_add("write", self.validate_fields)

    def validate_fields(self, *args):
        # Check if all required fields are non-empty
        if all([self.id_var.get(), self.FirstName_var.get(), self.MiddleName_var.get(), self.LastName_var.get(),
                self.course_var.get(), self.type_var.get(), self.role_var.get()]):
            # Enable the "Submit" button if all fields are filled
            self.submit_button.config(state=tk.NORMAL)
        else:
            # Disable the "Submit" button if any field is empty
            self.submit_button.config(state=tk.DISABLED)

    def show_confirmation(self):
        # Retrieve the form data from the input fields
        # Gather the entered details from the input fields
        id = self.id_entry.get()
        FirstName = self.FirstName_entry.get()
        MiddleName = self.MiddleName_entry.get()
        LastName = self.LastName_entry.get()
        selected_course = self.course_var.get()
        selected_role = self.role_var.get()
        selected_request = self.type_var.get()

        # Create a message for the confirmation box
        confirmation_message = f"ID Number: {id}\nFirst Name: {FirstName}\nMiddle Name: {MiddleName}\nLast Name: {LastName}\nCourse: {selected_course}\nRole in the University: {selected_role}\nType of Request: {selected_request}\nIs the information correct?"

        # Show a message box to confirm the entered details
        user_confirmation = messagebox.askyesno("Confirmation of Request", confirmation_message)

        if user_confirmation:
            # Save the data to the database
            self.save_data_to_database(id, FirstName, MiddleName, LastName, selected_course, selected_role,
                                       selected_request)

            # Show success message and navigate to the next page
            messagebox.showinfo("Success", "Data has been submitted.")
            self.controller.show_frame("MainMenu_Page")

            # Clear the input fields
            self.id_entry.delete(0, tk.END)
            self.FirstName_entry.delete(0, tk.END)
            self.MiddleName_entry.delete(0, tk.END)
            self.LastName_entry.delete(0, tk.END)
            self.course_var.set("")
            self.role_var.set("")
            self.type_var.set("")

        else:
            return None

    def save_data_to_database(self, id, FirstName, MiddleName, LastName, selected_course, selected_role,
                              selected_request):
        # Establish a connection to the MySQL database
        db_request = mysql.connector.connect(
            host="localhost",
            user="root",
            password="030702",
            database="db_test"
        )
        cursor = db_request.cursor()

        # Define the SQL query to insert data into the database table
        insert_query = "INSERT INTO tbl_request (id_number, FirstName, MiddleName, LastName, course, role, request) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        # Execute the query with the provided values
        data = (id, FirstName, MiddleName, LastName, selected_course, selected_role, selected_request)
        cursor.execute(insert_query, data)

        # Commit the changes to the database and close the connection
        db_request.commit()
        db_request.close()

    def cancel_form(self):
        # Switch back to the main menu page
        self.controller.show_frame("MainMenu_Page")

    def clear_form(self):
        # Clear the input fields
        self.id_var.set("")  # Clear the ID input field
        self.FirstName_var.set("")  # Clear the First Name input field
        self.MiddleName_var.set("")  # Clear the Middle Name input field
        self.LastName_var.set("")  # Clear the Last Name input field
        self.course_var.set("")  # Clear the Course selection
        self.type_var.set("")  # Clear the Type of Request selection
        self.role_var.set("")  # Clear the Role in University selection


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