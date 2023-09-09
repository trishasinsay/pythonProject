import tkinter as tk
import tkinter as ttk
import time
from tkinter import PhotoImage
import pygame.camera
import pygame.image
from tkinter import messagebox
import tkcalendar
from PIL import Image, ImageTk
import pyzbar.pyzbar as pyzbar
import cv2
import threading
import mysql.connector
import pytesseract
from PIL import Image, ImageTk
from tkinter import ttk
import pytesseract
import numpy as np
import webbrowser
from tkcalendar import Calendar

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=0)
        container.grid_columnconfigure(0, weight=0)

        self.frames = {}
        for F in (StartPage, MainMenu_Page, RequestPage, ValidationPage, RegistrationPage, MatchingPage, MakerPage, StudentPage, FacultyPage, AlumniPage, LibraryPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
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
        self.canvas.coords(sub_heading_label, self.winfo_screenwidth() // 2 + 210, self.winfo_screenheight() // 3 + 160)

        # Create the "Get Started" button
        get_started_button = tk.Button(self, text='Get Started', font=('inter', 20, 'bold'),
                                       command=self.on_get_started_button_click, bg='#5D1C1C', fg='white',
                                       width=20, height= 2)

        # Place the button below the sub-heading label
        self.canvas.create_window(self.winfo_screenwidth() // 2 + 210, self.winfo_screenheight() // 2 + 215,
                                  window=get_started_button)

    def on_get_started_button_click(self):
        # Switch to the main menu with three buttons
        main_menu_page_frame = MainMenu_Page(self.controller, self.controller)
        main_menu_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('MainMenu_Page')

class MainMenu_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#D8D8D8')
        self.controller = controller

        # Create a label for the RegistrationPage
        request_label = tk.Label(self, text="MAIN MENU", font=('caveat brush', 55), bg='#D8D8D8',
                                 fg='#5D1C1C')
        request_label.grid(row=0, column=1, pady=40, padx=20, sticky='N')

        # Add a label below the button
        label1 = tk.Label(self, text='ID VALIDATION', font=('inter', 25, 'bold'), background='#D8D8D8')
        label1.grid(row=0, column=0, pady=150, padx=120, sticky='nw')

        label2 = tk.Label(self, text='REQUEST ID', font=('inter', 25, 'bold'), background='#D8D8D8')
        label2.grid(row=0, column=1, pady=150, padx=60, sticky='n')

        label3 = tk.Label(self, text='ID MAKER', font=('inter', 25, 'bold'), background='#D8D8D8')
        label3.grid(row=0, column=2, pady=150, padx=50, sticky='n')


        # Load image for the button
        image1 = tk.PhotoImage(file='validation.png')
        image2 = tk.PhotoImage(file='requesting.png')
        image3 = tk.PhotoImage(file='maker.png')


        # Create the button with the background color and image on top
        button1 = tk.Button(self, image=image1, compound=tk.TOP, bg='#5D1C1C', height=370, width=300,
                            command=self.on_button1_click, bd=0)
        button1.grid(row=0, column=0, pady=200, padx=90, sticky='w')

        button2 = tk.Button(self, image=image2, compound=tk.TOP, bg='#5D1C1C', height=370, width=330,
                            command=self.on_button2_click, bd=0)
        button2.grid(row=0, column=1, pady=200, padx=20, sticky='w')

        button3 = tk.Button(self, image=image3, compound=tk.TOP, bg='#5D1C1C', height=370, width=300,
                            command=self.on_button3_click, bd=0)
        button3.grid(row=0, column=2, pady=200, padx=70, sticky='e')


        # Set the image as button attribute to avoid garbage collection
        button1.image = image1
        button2.image = image2
        button3.image = image3


    def on_button1_click(self):
        # Switch to the main menu with three buttons
        validation_page_frame = ValidationPage(self.controller, self.controller)
        validation_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('ValidationPage')

    def on_button2_click(self):
        # Switch to the main menu with three buttons
        request_page_frame = ValidationPage(self.controller, self.controller)
        request_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('RequestPage')

    def on_button3_click(self):
        # Handle button 3 click event
        maker_page_frame = MakerPage(self.controller, self.controller)
        maker_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('MakerPage')

class ValidationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#D8D8D8')
        self.controller = controller

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

        # Define the background color for the scan button
        scan_button_bg_color = '#5D1C1C'

        # Create Scan button with background color
        self.scan_button = tk.Button(self, text='TAP TO SCAN YOUR ID', font=('inter', 25, 'bold'), fg='white', bg=scan_button_bg_color,
                                     width=25, command=self.start_qr_scan_thread)
        self.scan_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # Adjust the values of relx and rely

        # Create the camera preview label
        self.camera_preview_label = tk.Label(self)
        self.camera_preview_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # Initialize variables to hold the camera capture and thread state
        self.cap = None
        self.thread_running = False

    def start_qr_scan_thread(self):
        # Create a new thread to run the QR code scanning process and camera preview
        qr_scan_thread = threading.Thread(target=self.start_qr_scan)
        qr_scan_thread.start()

    def open_registration_page(self, data_list):
        if len(data_list) >= 4:
            id_number, name, course, qr_code_number = data_list

            # Transition to the RegistrationPage and pass the scanned data
            self.controller.show_frame("RegistrationPage")
            self.controller.frames["RegistrationPage"].populate_data(id_number, name, course, qr_code_number)
        else:
            messagebox.showerror('Error', 'Invalid QR Code Data')

    def start_qr_scan(self):
        # Start the camera and create the camera preview thread
        self.cap = cv2.VideoCapture(0)
        self.thread_running = True
        self.camera_preview_thread = threading.Thread(target=self.update_camera_preview)
        self.camera_preview_thread.start()

    def scan_qr_code(self):
        # Capture the scanned image data
        self.scanned_image_data = self.camera_preview_label.get_image_data()

        # Navigate to the MatchingPage
        self.controller.show_frame("MatchingPage")

        # Create a label for the camera preview dynamically
        # Start the camera preview in the label
        self.camera_preview = tk.Label(self)
        self.camera_preview.place(relx=0.5, rely=0.4, anchor=tk.CENTER)


    def update_camera_preview(self):
        while self.thread_running:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Convert the frame to ImageTk format to display in the label
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(image=image)

            # Update the camera preview label with the new frame
            self.camera_preview_label.config(image=photo)
            self.camera_preview_label.image = photo

            decoded_objects = pyzbar.decode(frame)
            if decoded_objects:
                qr_code_data = decoded_objects[0].data.decode('utf-8')
                messagebox.showinfo('QR Code Scanned', f'Success! QR Code: {qr_code_data}')

                # Stop the camera and thread after scanning
                self.stop_qr_scan()
                # Close the camera frame after a delay of 2 seconds
                self.after(200, self.close_camera_preview)

                # Split the QR code data by spaces and pass them to the registration page
                data_list = qr_code_data.split()
                self.after(200, lambda: self.open_registration_page(data_list))

        self.cap.release()

    def stop_qr_scan(self):
        self.thread_running = False

    def close_camera_preview(self):
        # Clear the camera preview label
        if self.camera_preview_label:
            self.camera_preview_label.destroy()
            self.camera_preview_label = None

class RegistrationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#EFEFEF')  # Set the background color for the entire page
        self.controller = controller

        # Create a colored square background frame to hold the labels and input fields
        form_frame = tk.Frame(self, bg='#5D1C1C', pady=20, width=180, height=200)
        form_frame.pack(expand=True, fill=tk.BOTH)  # Allow the form_frame to fill available space

        # Center the form_frame within the window
        form_frame.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        # Create a label for the RegistrationPage
        registration_label = tk.Label(form_frame, text="Student's Information", font=('caveat brush', 30), bg='#5D1C1C',
                                      fg='#FFFFFF')
        registration_label.grid(row=0, column=0, pady=20, padx=350, sticky='nwe')

        # Create input fields for name, course, ID number, and QR code number
        name_label = tk.Label(form_frame, text='Name:', font=('inter', 18, 'bold'), bg='#5D1C1C', fg='#FFFFFF')
        name_label.grid(row=2, column=0, padx=315, pady=25, sticky='w')

        self.name_entry = tk.Entry(form_frame, font=('inter', 16))
        self.name_entry.grid(row=2, column=0, padx=400, pady=25, sticky='w')

        course_label = tk.Label(form_frame, text='Course:', font=('inter', 18, 'bold'), bg='#5D1C1C', fg='#FFFFFF')
        course_label.grid(row=3, column=0, padx=300, sticky='w')

        self.course_entry = tk.Entry(form_frame, font=('inter', 16))
        self.course_entry.grid(row=3, column=0, padx=400, pady=25, sticky='w')

        id_label = tk.Label(form_frame, text='ID Number:', font=('inter', 18, 'bold'), bg='#5D1C1C', fg='#FFFFFF')
        id_label.grid(row=4, column=0, padx=260, sticky='w')

        self.id_entry = tk.Entry(form_frame, font=('inter', 16))
        self.id_entry.grid(row=4, column=0, padx=400, pady=25, sticky='w')

        qr_code_label = tk.Label(form_frame, text='QR Code Number:', font=('inter', 18, 'bold'), bg='#5D1C1C', fg='#FFFFFF')
        qr_code_label.grid(row=5, column=0, padx=180, pady=15, sticky='w')

        self.qr_code_entry = tk.Entry(form_frame, font=('inter', 16))
        self.qr_code_entry.grid(row=5, column=0, padx=400, pady=15, sticky='w')


        # Create the Proceed button, but set it to be disabled initially
        proceed_button = tk.Button(form_frame, text='Proceed', font=('caveat brush', 20), command=self.proceed_form,
                                   width=10, bg='#5D1C1C', fg='#FFFFFF')
        proceed_button.grid(row=10, column=0, columnspan=1, pady=20, padx=400, sticky='se')

        # Create the cancel button
        cancel_button = tk.Button(form_frame, text='Cancel', font=('caveat brush', 20), command=self.cancel_form, bg='#5D1C1C',
                                  width=10, fg='#FFFFFF')
        cancel_button.grid(row=10, column=0, columnspan=1, pady=20, padx=360, sticky='sw')

    def populate_data(self, id_number, name, course, qr_code_number):
        # Populate the data from the QR code into the registration form
        self.id_entry.insert(0, id_number)
        self.name_entry.insert(0, name)
        self.course_entry.insert(0, course)
        self.qr_code_entry.insert(0, qr_code_number)

        # Disable editing for populated fields
        self.id_entry.config(state="readonly")
        self.name_entry.config(state="readonly")
        self.course_entry.config(state="readonly")
        self.qr_code_entry.config(state="readonly")

    def proceed_form(self):
        # Retrieve the form data from the input fields
        id_number = self.id_entry.get()
        name = self.name_entry.get()
        course = self.course_entry.get()
        qr_code_number = self.qr_code_entry.get()

        # You can now use this data as needed, for example, display a message with the data
        message = f'ID Number: {id_number}\nName: {name}\nCourse: {course}\nQR Code Number: {qr_code_number}'
        user_confirmation = tk.messagebox.askokcancel('Student Information', message)

        if user_confirmation:
            # Save the data to the database (example using SQLite)
            self.save_data_to_database(id_number, name, course, qr_code_number)

            messagebox.showinfo("Success", "Data has been submitted.")
            self.controller.show_frame("MainMenu_Page")

            # Clear the input fields
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.course_entry.delete(0, tk.END)
            self.qr_code_entry.delete(0, tk.END)

        else:
            return None

        # Direct to the matching page after saving data
        self.controller.show_frame("MatchingPage")

    def save_data_to_database(self, id_number, name, course, qr_code_number):
        # Replace the following with your MySQL database credentials
        # Replace 'database_name', 'table_name', and 'your_mysql_username' with your database and table information

        db_temp = mysql.connector.connect(
            host="localhost",
            user="root",
            password="030702",
            database="db_temp"
        )
        # Establish a connection to the MySQL database
        cursor = db_temp.cursor()

        # Define the SQL query to insert data into the database table
        insert_query = "INSERT INTO tbl_temp (id_number, name, course, qr_code_number) VALUES (%s, %s, %s, %s)"

        # Execute the query with the provided values
        data = (id_number, name, course, qr_code_number)
        cursor.execute(insert_query, data)

        # Commit the changes to the database and close the connection
        db_temp.commit()
        db_temp.close()

    def cancel_form(self):
        # Switch back to the main menu page
        self.controller.show_frame("MainMenu_Page")

class MatchingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.cap = None
        self.photo = None
        self.camera_preview_initialized = False

        # Create a canvas to display the camera preview
        self.camera_canvas = tk.Canvas(self, width=640, height=480)
        self.camera_canvas.pack()

        # Create a label for the text extraction results
        self.text_result_label = tk.Label(self, text='', font=('inter', 14), fg='white', bg='#5D1C1C')
        self.text_result_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Define the background color for the scan button
        scan_button_bg_color = '#5D1C1C'

        # Create Scan button with background color
        self.scan_button = tk.Button(self, text='TAP TO SCAN YOUR COR', font=('caveat brush', 18), fg='white', bg=scan_button_bg_color,
                                     width=28, command=self.capture_and_extract)
        self.scan_button.place(relx=0.5, rely=0.5, anchor=tk.S)

        # Call the function to initialize and display the camera preview
        self.initialize_camera_preview()

    def initialize_camera_preview(self):
        if not self.camera_preview_initialized:
            # Open the camera (replace '0' with the correct camera index or device name)
            self.cap = cv2.VideoCapture(1)
            self.camera_preview_initialized = True

        self.update_camera_preview()

    def update_camera_preview(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        if ret:
            # Enhance the color (contrast stretching)
            frame = self.enhance_color(frame)

            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Extract text and draw a bounding box
            extracted_text, bbox_image = self.extract_text_from_image(frame_rgb)
            self.text_result_label.config(text=extracted_text)

            # Convert the frame with the bounding box to PhotoImage
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(bbox_image))

            # Update the canvas with the new frame
            self.camera_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Schedule the update method to be called again after 10ms
        self.after(10, self.update_camera_preview)

    def capture_and_extract(self):
        if not self.camera_preview_initialized:
            self.initialize_camera_preview()

        ret, frame = self.cap.read()
        if ret:
            extracted_text, _ = self.extract_text_from_image(frame)
            self.text_result_label.config(text=extracted_text)
            print("Extracted Text:", extracted_text)

        else:
            pass

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
        # Replace with your database credentials
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="030702",
            database="db_temp"
        )

        cursor = db.cursor()
        cursor.execute("SELECT course FROM tbl_temp WHERE course = %s", (extracted_text,))
        result = cursor.fetchone()

        db.close()

        # If a matching record is found in the database, return True
        return result is not None

class RequestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#EFEFEF')  # Set the background color for the entire page
        self.controller = controller

        # Create a colored square background frame to hold the labels and input fields
        form_frame = tk.Frame(self, bg='#5D1C1C',padx=50, pady=50)
        form_frame.pack(expand=True, fill=tk.BOTH)  # Allow the form_frame to fill available space

        # Create a label for the RegistrationPage
        request_label = tk.Label(form_frame, text="REQUEST FORM", font=('inter', 30, 'bold'), bg='#5D1C1C',
                                 fg='#FFFFFF')
        request_label.grid(row=0, column=1, columnspan=3, pady=18, sticky='N')

        note_label = tk.Label(form_frame,
                              text="Kindly provide the complete information needed in this online form.\n\n"
                                   "There is a 150 pesos ID fee to be paid at the Cashier's Office for the replacement.",
                              font=('inter', 15), bg='#5D1C1C', fg='#FFFFFF')
        note_label.grid(row=2, column=1, padx=50, pady=30, sticky='w')


        id_label = tk.Label(form_frame, text='ID Number:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        id_label.grid(row=4, column=0, padx=10, pady=15, sticky='e')

        self.id_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.id_entry.grid(row=4, column=1, padx=10, pady=15, sticky='w')

        # Create input fields for name, course, ID number, and QR code number
        FirstName_label = tk.Label(form_frame, text='First Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        FirstName_label.grid(row=5, column=0, padx=10, pady=15, sticky='e')

        self.FirstName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.FirstName_entry.grid(row=5, column=1, padx=10, pady=15, sticky='w')

        MiddleName_label = tk.Label(form_frame, text='Middle Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        MiddleName_label.grid(row=6, column=0, padx=10, pady=15, sticky='e')

        self.MiddleName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.MiddleName_entry.grid(row=6, column=1, padx=10, pady=15, sticky='w')

        LastName_label = tk.Label(form_frame, text='Last Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        LastName_label.grid(row=7, column=0, padx=10, pady=15, sticky='e')

        self.LastName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.LastName_entry.grid(row=7, column=1, padx=10, pady=15, sticky='w')

        course_label = tk.Label(form_frame, text='Course:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        course_label.grid(row=8, column=0, padx=10, pady=15, sticky='e')

        # Create a Combobox for the "Course" field
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

        # Create the Proceed button, but set it to be disabled initially
        submit_button = tk.Button(form_frame, text='Submit', font=('inter', 18), command=self.show_confirmation, bg='#5D1C1C', fg='#FFFFFF')
        submit_button.grid(row=10, column=1, columnspan=1, padx=15,  pady=20)

        # Create the cancel button
        cancel_button = tk.Button(form_frame, text='Cancel', font=('inter', 18), command=self.cancel_form, bg='#5D1C1C', fg='#FFFFFF')
        cancel_button.grid(row=10, column=0, columnspan=2, padx=15, pady=20)

    def show_confirmation(self):
        # Retrieve the form data from the input fields
        # Gather the entered details from the input fields
        id = self.id_entry.get()
        FirstName = self.FirstName_entry.get()
        MiddleName = self.MiddleName_entry.get()
        LastName = self.LastName_entry.get()
        selected_course = self.course_var.get()


        # Create a message for the confirmation box
        confirmation_message = f"ID Number: {id}\nFirst Name: {FirstName}\nMiddle Name: {MiddleName}\nLast Name: {LastName}\nCourse: {selected_course}\nIs the information correct?"

        # Show a message box to confirm the entered details
        user_confirmation = messagebox.askyesno("Confirmation of Request", confirmation_message)

        if user_confirmation:
            # Save the data to the database
            self.save_data_to_database(id, FirstName, MiddleName, LastName, selected_course)

            # Show success message and navigate to the next page
            messagebox.showinfo("Success", "Data has been submitted.")
            self.controller.show_frame("MainMenu_Page")

            # Clear the input fields
            self.id_entry.delete(0, tk.END)
            self.FirstName_entry.delete(0, tk.END)
            self.MiddleName_entry.delete(0, tk.END)
            self.LastName_entry.delete(0, tk.END)
            self.course_var.set("")

        else:
            return None

    def save_data_to_database(self, id, FirstName, MiddleName, LastName, selected_course):
        # Establish a connection to the MySQL database
        db_request = mysql.connector.connect(
            host="localhost",
            user="root",
            password="030702",
            database="db_test"
        )
        cursor = db_request.cursor()

        # Define the SQL query to insert data into the database table
        insert_query = "INSERT INTO tbl_request (id_number, FirstName, MiddleName, LastName, course) VALUES (%s, %s, %s, %s, %s)"

        # Execute the query with the provided values
        data = (id, FirstName, MiddleName, LastName, selected_course)
        cursor.execute(insert_query, data)

        # Commit the changes to the database and close the connection
        db_request.commit()
        db_request.close()

    def cancel_form(self):
        # Switch back to the main menu page
        self.controller.show_frame("MainMenu_Page")

class MakerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#D8D8D8')
        self.controller = controller

        # Create a label for the RegistrationPage
        request_label = tk.Label(self, text="TUPC ID CARD MAKER", font=('caveat brush', 45), bg='#D8D8D8',
                                 fg='#5D1C1C')
        request_label.grid(row=0, column=1, columnspan=2, pady=40, sticky='N')

        # Add a label below the button
        label1 = tk.Label(self, text='STUDENT', font=('inter', 25, 'bold'), background='#D8D8D8')
        label1.grid(row=0, column=0, pady=150, padx=100, sticky='nw')

        label2 = tk.Label(self, text='FACULTY', font=('inter', 25, 'bold'), background='#D8D8D8')
        label2.grid(row=0, column=1, pady=150, padx=50, sticky='n')

        label3 = tk.Label(self, text='ALUMNI', font=('inter', 25, 'bold'), background='#D8D8D8')
        label3.grid(row=0, column=2, pady=150, padx=50, sticky='n')

        label4 = tk.Label(self, text='LIBRARY', font=('inter', 25, 'bold'), background='#D8D8D8')
        label4.grid(row=0, column=3, pady=150, padx=60, sticky='ne')

        # Load image for the button
        image1 = tk.PhotoImage(file='students.png')
        image2 = tk.PhotoImage(file='faculty.png')
        image3 = tk.PhotoImage(file='alumni-icon.png')
        image4 = tk.PhotoImage(file='library.png')

        # Create the button with the background color and image on top
        button1 = tk.Button(self, image=image1, compound=tk.TOP, bg='#5D1C1C', height=370, width=270,
                            command=self.on_button1_click, bd=0)
        button1.grid(row=0, column=0, pady=200, padx=50, sticky='w')

        button2 = tk.Button(self, image=image2, compound=tk.TOP, bg='#5D1C1C', height=370, width=270,
                            command=self.on_button2_click, bd=0)
        button2.grid(row=0, column=1, pady=200, padx=1, sticky='w')

        button3 = tk.Button(self, image=image3, compound=tk.TOP, bg='#5D1C1C', height=370, width=270,
                            command=self.on_button3_click, bd=0)
        button3.grid(row=0, column=2, pady=200, padx=50, sticky='e')

        button4 = tk.Button(self, image=image4, compound=tk.TOP, bg='#5D1C1C', height=370, width=270,
                            command=self.on_button4_click, bd=0)
        button4.grid(row=0, column=3, pady=200, padx=3, sticky='e')


        # Set the image as button attribute to avoid garbage collection
        button1.image = image1
        button2.image = image2
        button3.image = image3
        button4.image = image4

        back_button = tk.PhotoImage(file='back.png')

        # Create the button with the background color and image on top
        cancel_button = tk.Button(self, image=back_button, bg='#D8D8D8', height=50, width=50,
                                  command=self.cancel_form, bd=0)
        cancel_button.grid(row=0, column=0, pady=5, padx=10, sticky='nw')

        # Set the image as button attribute to avoid garbage collection
        cancel_button.image = back_button

    def cancel_form(self):
        # Switch back to the main menu page
        self.controller.show_frame("MainMenu_Page")

    def on_button1_click(self):
        # Switch to the main menu with three buttons
        student_page_frame = ValidationPage(self.controller, self.controller)
        student_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('StudentPage')

    def on_button2_click(self):
        # Switch to the main menu with three buttons
        faculty_page_frame = ValidationPage(self.controller, self.controller)
        faculty_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('FacultyPage')

    def on_button3_click(self):
        # Handle button 3 click event
        alumni_page_frame = MakerPage(self.controller, self.controller)
        alumni_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('AlumniPage')

    def on_button4_click(self):
        # Handle button 3 click event
        library_page_frame = MakerPage(self.controller, self.controller)
        library_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('LibraryPage')

class StudentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#5D1C1C')  # Set the background color for the entire page
        self.controller = controller

        # Create a label for the RegistrationPage
        studentID_label = tk.Label(self, text="STUDENT ID INFORMATION FORM", font=('caveat brush', 40), bg='#5D1C1C',
                                 fg='#FFFFFF')
        studentID_label.grid(row=0, column=1, pady=50, padx=110, sticky='NW')

        note_label = tk.Label(self,
                              text="NOTE: Kindly provide the complete information needed in this form for your ID.\n\n",
                              font=('inter', 15, 'bold'), bg='#5D1C1C', fg='#FFFFFF')
        note_label.grid(row=0, column=1, padx=60, pady=140, sticky='NW')

        id_label = tk.Label(self, text='ID Number:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        id_label.grid(row=0, rowspan=1, column=0, columnspan=2, padx=80, pady=190, sticky='W')

        self.id_entry = tk.Entry(self, font=('inter', 14), width=30)
        self.id_entry.grid(row=0, rowspan=1, column=1, columnspan=1,  padx=2, pady=190, sticky='W')

        # Create input fields for name, course, ID number, and QR code number
        FirstName_label = tk.Label(self, text='First Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        FirstName_label.grid(row=0, rowspan=2, column=0, columnspan=1,  padx=80, pady=200, sticky='W')

        self.FirstName_entry = tk.Entry(self, font=('inter', 14), width=30)
        self.FirstName_entry.grid(row=0, rowspan=2, column=1, columnspan=1,  padx=2, pady=200, sticky='W')

        MiddleInitial_label = tk.Label(self, text='Middle Initial:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        MiddleInitial_label.grid(row=0, rowspan=3, column=0, columnspan=1,  padx=80, pady=250, sticky='W')

        self.MiddleInitial_entry = tk.Entry(self, font=('inter', 14), width=30)
        self.MiddleInitial_entry.grid(row=0, rowspan=3, column=1, columnspan=1,  padx=2, pady=250, sticky='W')

        LastName_label = tk.Label(self, text='Last Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        LastName_label.grid(row=0, rowspan=4, column=0, columnspan=1,  padx=80, pady=300, sticky='W')

        self.LastName_entry = tk.Entry(self, font=('inter', 14), width=30)
        self.LastName_entry.grid(row=0, rowspan=4, column=1, columnspan=1,  padx=2, pady=300, sticky='W')

        course_label = tk.Label(self, text='Course:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        course_label.grid(row=0, rowspan=5, column=0, columnspan=1,  padx=80, pady=350, sticky='W')

        # Create a Combobox for the "Course" field
        self.course_var = tk.StringVar()
        course_combobox = ttk.Combobox(self, textvariable=self.course_var,
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
                                       font=('inter', 12), state="readonly", width=65)
        course_combobox.grid(row=0, rowspan=5, column=1, columnspan=1,  padx=2, pady=350, sticky='W')

        signature_label = tk.Label(self, text='Signature:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        signature_label.grid(row=0, rowspan=6, column=0, columnspan=1, padx=80, pady=400, sticky='W')

        # Create a canvas for drawing
        self.canvas1 = tk.Canvas(self, bg='white', width=600, height=130)
        self.canvas1.grid(row=0, rowspan=7, column=1, columnspan=1,  padx=2, pady=5, sticky='w')

        # Bind mouse events to the canvas
        self.canvas1.bind("<Button-1>", self.start_drawing)
        self.canvas1.bind("<B1-Motion>", self.draw)
        self.canvas1.bind("<ButtonRelease-1>", self.stop_drawing)

        self.is_drawing = False
        self.last_x = 0
        self.last_y = 0

        self.button_clear = tk.Button(self, text='Clear', font=('inter', 15), command=self.clear_canvas, bg='#5D1C1C', fg='#FFFFFF',  width=10)
        self.button_clear.grid(row=0, rowspan=8, column=1,  padx=275, pady=570, sticky='se')

        # Create the camera preview label
        self.camera_preview_label = tk.Label(self, width=500, height=80, bg='white')
        self.camera_preview_label.place(relx=0.9, rely=0.3, anchor=tk.E, width=300, height=300)

        # Create a canvas for displaying the captured image
        self.canvas = tk.Canvas(self, bg='white', width=300, height=300)
        self.canvas.place(relx=0.9, rely=0.3, anchor=tk.E, width=300, height=300)

        # Initialize a variable to store the captured image
        self.captured_image = None

        # Create the Proceed button, but set it to be disabled initially
        capture_button = tk.Button(self, text='Take Picture', font=('inter', 16), command=self.show_popup, bg='#5D1C1C',
                             fg='#FFFFFF', width=12)
        capture_button.grid(row=0, rowspan=7, column=1, columnspan=1, padx=35, pady=160, sticky='e')


        # Create the Proceed button, but set it to be disabled initially
        next_button = tk.Button(self, text='Next', font=('inter', 18), command=self.show_confirmation, bg='#5D1C1C', fg='#FFFFFF',  width=10)
        next_button.grid(row=0, rowspan=9, column=1,  padx=35, pady=150, sticky='e')

        back_button = tk.PhotoImage(file='back.png')

        # Create the button with the background color and image on top
        cancel_button = tk.Button(self, image=back_button, bg='#5D1C1C', height=50, width=50,
                              command=self.cancel_form, bd=0)
        cancel_button.grid(row=0, column=0, pady=10, padx=7, sticky='nw')

        # Set the image as button attribute to avoid garbage collection
        cancel_button.image = back_button

    def start_drawing(self, event):
        self.is_drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.is_drawing:
            self.canvas1.create_line(self.last_x, self.last_y, event.x, event.y, fill='black', width=2)
            self.last_x = event.x
            self.last_y = event.y

    def stop_drawing(self, event):
        self.is_drawing = False

    def show_popup(self):
        # Create a Toplevel window (pop-up)
        popup = tk.Toplevel(self, bg='#5D1C1C')

        # Set the title and size of the pop-up window
        popup.title("Capture Image")
        popup.geometry("800x600")

        # Add a canvas for the camera preview
        camera_canvas = tk.Canvas(popup, width=640, height=480, bg='#5D1C1C')
        camera_canvas.pack(pady=20)

        # Add a button for capturing an image
        capture_button = tk.Button(popup, text="Capture", font=('inter', 18), command=lambda: self.capture_image(camera_canvas), bg='#5D1C1C', fg='#FFFFFF', width=10)
        capture_button.pack()

        # Initialize and start the camera preview
        self.initialize_camera_preview(camera_canvas)

    def initialize_camera_preview(self, canvas):
        self.cap = cv2.VideoCapture(0)
        self.update_camera_preview(canvas)

    def update_camera_preview(self, canvas):
        ret, frame = self.cap.read()

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            canvas.photo = photo

        canvas.after(10, lambda: self.update_camera_preview(canvas))

    def capture_image(self, canvas):
        ret, frame = self.cap.read()
        if ret:
            # Save the captured image to a file or perform further processing
            cv2.imwrite("captured_image.png", frame)
            self.captured_image = Image.open("captured_image.png")

            # Display the captured image in the canvas
            if self.captured_image:
                photo = ImageTk.PhotoImage(image=self.captured_image)
                canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                canvas.photo = photo

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (400, 200), "white")
        self.draw = ImageDraw.Draw(self.image)

    def show_confirmation(self):
        # Retrieve the form data from the input fields
        # Gather the entered details from the input fields
        id = self.id_entry.get()
        FirstName = self.FirstName_entry.get()
        MiddleInitial = self.MiddleInitial_entry.get()
        LastName = self.LastName_entry.get()
        selected_course = self.course_var.get()

        # Clear the input fields
        self.id_entry.delete(0, tk.END)
        self.FirstName_entry.delete(0, tk.END)
        self.MiddleInitial_entry.delete(0, tk.END)
        self.LastName_entry.delete(0, tk.END)
        self.course_var.set("")

        image = self.canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(image.encode('utf-8')))
        img.save('signature.png')

        # Create a message for the confirmation box
        confirmation_message = f"ID Number: {id}\nFirst Name: {FirstName}\nMiddle Initial: {MiddleInitial}\nLast Name: {LastName}\nCourse: {selected_course}\nIs the information correct?"

        # Show a message box to confirm the entered details
        user_confirmation = messagebox.askyesno("Confirmation of Request", confirmation_message)

        if user_confirmation:
            # Save the data to the database
            self.save_data_to_database(id, FirstName, MiddleInitial, LastName, selected_course)

            # Show success message and navigate to the next page
            messagebox.showinfo("Success", "Data has been submitted.")
            self.controller.show_frame("MainMenu_Page")

    def save_data_to_database(self, id, FirstName, MiddleInitial, LastName, selected_course):
        # Establish a connection to the MySQL database
        db_request = mysql.connector.connect(
            host="localhost",
            user="root",
            password="030702",
            database="db_test"
        )
        cursor = db_request.cursor()

        # Define the SQL query to insert data into the database table
        insert_query = "INSERT INTO tbl_request (id_number, FirstName, MiddleInitial, LastName, course) VALUES (%s, %s, %s, %s, %s)"

        # Execute the query with the provided values
        data = (id, FirstName, MiddleInitial, LastName, selected_course)
        cursor.execute(insert_query, data)

        # Commit the changes to the database and close the connection
        db_request.commit()
        db_request.close()


    def cancel_form(self):
        # Switch back to the main menu page
        self.controller.show_frame("MakerPage")

class FacultyPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#EFEFEF')  # Set the background color for the entire page
        self.controller = controller

        # Create a colored square background frame to hold the labels and input fields
        form_frame = tk.Frame(self, bg='#5D1C1C',padx=50, pady=50)
        form_frame.pack(expand=True, fill=tk.BOTH)  # Allow the form_frame to fill available space

        # Create a label for the RegistrationPage
        request_label = tk.Label(form_frame, text="FACULTY ID INFORMATION", font=('inter', 30, 'bold'), bg='#5D1C1C',
                                 fg='#FFFFFF')
        request_label.grid(row=0, column=1, columnspan=3, pady=18, sticky='N')

        note_label = tk.Label(form_frame,
                              text="Kindly provide the complete information needed in this online form.\n\n"
                                   "There is a 150 pesos ID fee to be paid at the Cashier's Office for the replacement.",
                              font=('inter', 15), bg='#5D1C1C', fg='#FFFFFF')
        note_label.grid(row=2, column=1, padx=50, pady=30, sticky='w')


        id_label = tk.Label(form_frame, text='ID Number:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        id_label.grid(row=4, column=0, padx=10, pady=15, sticky='e')

        self.id_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.id_entry.grid(row=4, column=1, padx=10, pady=15, sticky='w')

        # Create input fields for name, course, ID number, and QR code number
        FirstName_label = tk.Label(form_frame, text='First Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        FirstName_label.grid(row=5, column=0, padx=10, pady=15, sticky='e')

        self.FirstName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.FirstName_entry.grid(row=5, column=1, padx=10, pady=15, sticky='w')

        MiddleName_label = tk.Label(form_frame, text='Middle Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        MiddleName_label.grid(row=6, column=0, padx=10, pady=15, sticky='e')

        self.MiddleName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.MiddleName_entry.grid(row=6, column=1, padx=10, pady=15, sticky='w')

        LastName_label = tk.Label(form_frame, text='Last Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        LastName_label.grid(row=7, column=0, padx=10, pady=15, sticky='e')

        self.LastName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.LastName_entry.grid(row=7, column=1, padx=10, pady=15, sticky='w')

        course_label = tk.Label(form_frame, text='Course:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        course_label.grid(row=8, column=0, padx=10, pady=15, sticky='e')

        # Create a Combobox for the "Course" field
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

        # Create the Proceed button, but set it to be disabled initially
        submit_button = tk.Button(form_frame, text='Submit', font=('inter', 18), command=self.show_confirmation, bg='#5D1C1C', fg='#FFFFFF')
        submit_button.grid(row=10, column=1, columnspan=1, padx=15,  pady=20)

        # Create the cancel button
        cancel_button = tk.Button(form_frame, text='Cancel', font=('inter', 18), command=self.cancel_form, bg='#5D1C1C', fg='#FFFFFF')
        cancel_button.grid(row=10, column=0, columnspan=2, padx=15, pady=20)

    def show_confirmation(self):
        # Retrieve the form data from the input fields
        # Gather the entered details from the input fields
        id = self.id_entry.get()
        FirstName = self.FirstName_entry.get()
        MiddleName = self.MiddleName_entry.get()
        LastName = self.LastName_entry.get()
        selected_course = self.course_var.get()

        # Clear the input fields
        self.id_entry.delete(0, tk.END)
        self.FirstName_entry.delete(0, tk.END)
        self.MiddleName_entry.delete(0, tk.END)
        self.LastName_entry.delete(0, tk.END)
        self.course_var.set("")

        # Create a message for the confirmation box
        confirmation_message = f"ID Number: {id}\nFirst Name: {FirstName}\nMiddle Name: {MiddleName}\nLast Name: {LastName}\nCourse: {selected_course}\nIs the information correct?"

        # Show a message box to confirm the entered details
        user_confirmation = messagebox.askyesno("Confirmation of Request", confirmation_message)

        if user_confirmation:
            # Save the data to the database
            self.save_data_to_database(id, FirstName, MiddleName, LastName, selected_course)

            # Show success message and navigate to the next page
            messagebox.showinfo("Success", "Data has been submitted.")
            self.controller.show_frame("MainMenu_Page")

    def save_data_to_database(self, id, FirstName, MiddleName, LastName, selected_course):
        # Establish a connection to the MySQL database
        db_request = mysql.connector.connect(
            host="localhost",
            user="root",
            password="030702",
            database="db_test"
        )
        cursor = db_request.cursor()

        # Define the SQL query to insert data into the database table
        insert_query = "INSERT INTO tbl_request (id_number, FirstName, MiddleName, LastName, course) VALUES (%s, %s, %s, %s, %s)"

        # Execute the query with the provided values
        data = (id, FirstName, MiddleName, LastName, selected_course)
        cursor.execute(insert_query, data)

        # Commit the changes to the database and close the connection
        db_request.commit()
        db_request.close()

    def cancel_form(self):
        # Switch back to the main menu page
        self.controller.show_frame("MakerPage")

class AlumniPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#EFEFEF')  # Set the background color for the entire page
        self.controller = controller

        # Create a colored square background frame to hold the labels and input fields
        form_frame = tk.Frame(self, bg='#5D1C1C',padx=50, pady=50)
        form_frame.pack(expand=True, fill=tk.BOTH)  # Allow the form_frame to fill available space

        # Create a label for the RegistrationPage
        request_label = tk.Label(form_frame, text="ALUMNI ID INFORMATION FORM", font=('inter', 30, 'bold'), bg='#5D1C1C',
                                 fg='#FFFFFF')
        request_label.grid(row=0, column=1, columnspan=3, pady=18, sticky='N')

        note_label = tk.Label(form_frame,
                              text="Kindly provide the complete information needed in this online form.\n\n"
                                   "There is a 150 pesos ID fee to be paid at the Cashier's Office for the replacement.",
                              font=('inter', 15), bg='#5D1C1C', fg='#FFFFFF')
        note_label.grid(row=2, column=1, padx=50, pady=30, sticky='w')


        id_label = tk.Label(form_frame, text='ID Number:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        id_label.grid(row=4, column=0, padx=10, pady=15, sticky='e')

        self.id_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.id_entry.grid(row=4, column=1, padx=10, pady=15, sticky='w')

        # Create input fields for name, course, ID number, and QR code number
        FirstName_label = tk.Label(form_frame, text='First Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        FirstName_label.grid(row=5, column=0, padx=10, pady=15, sticky='e')

        self.FirstName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.FirstName_entry.grid(row=5, column=1, padx=10, pady=15, sticky='w')

        MiddleName_label = tk.Label(form_frame, text='Middle Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        MiddleName_label.grid(row=6, column=0, padx=10, pady=15, sticky='e')

        self.MiddleName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.MiddleName_entry.grid(row=6, column=1, padx=10, pady=15, sticky='w')

        LastName_label = tk.Label(form_frame, text='Last Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        LastName_label.grid(row=7, column=0, padx=10, pady=15, sticky='e')

        self.LastName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.LastName_entry.grid(row=7, column=1, padx=10, pady=15, sticky='w')

        course_label = tk.Label(form_frame, text='Course:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        course_label.grid(row=8, column=0, padx=10, pady=15, sticky='e')

        # Create a Combobox for the "Course" field
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

        # Create the Proceed button, but set it to be disabled initially
        submit_button = tk.Button(form_frame, text='Submit', font=('inter', 18), command=self.show_confirmation, bg='#5D1C1C', fg='#FFFFFF')
        submit_button.grid(row=10, column=1, columnspan=1, padx=15,  pady=20)

        # Create the cancel button
        cancel_button = tk.Button(form_frame, text='Cancel', font=('inter', 18), command=self.cancel_form, bg='#5D1C1C', fg='#FFFFFF')
        cancel_button.grid(row=10, column=0, columnspan=2, padx=15, pady=20)

    def show_confirmation(self):
        # Retrieve the form data from the input fields
        # Gather the entered details from the input fields
        id = self.id_entry.get()
        FirstName = self.FirstName_entry.get()
        MiddleName = self.MiddleName_entry.get()
        LastName = self.LastName_entry.get()
        selected_course = self.course_var.get()

        # Clear the input fields
        self.id_entry.delete(0, tk.END)
        self.FirstName_entry.delete(0, tk.END)
        self.MiddleName_entry.delete(0, tk.END)
        self.LastName_entry.delete(0, tk.END)
        self.course_var.set("")

        # Create a message for the confirmation box
        confirmation_message = f"ID Number: {id}\nFirst Name: {FirstName}\nMiddle Name: {MiddleName}\nLast Name: {LastName}\nCourse: {selected_course}\nIs the information correct?"

        # Show a message box to confirm the entered details
        user_confirmation = messagebox.askyesno("Confirmation of Request", confirmation_message)

        if user_confirmation:
            # Save the data to the database
            self.save_data_to_database(id, FirstName, MiddleName, LastName, selected_course)

            # Show success message and navigate to the next page
            messagebox.showinfo("Success", "Data has been submitted.")
            self.controller.show_frame("MainMenu_Page")

    def save_data_to_database(self, id, FirstName, MiddleName, LastName, selected_course):
        # Establish a connection to the MySQL database
        db_request = mysql.connector.connect(
            host="localhost",
            user="root",
            password="030702",
            database="db_test"
        )
        cursor = db_request.cursor()

        # Define the SQL query to insert data into the database table
        insert_query = "INSERT INTO tbl_request (id_number, FirstName, MiddleName, LastName, course) VALUES (%s, %s, %s, %s, %s)"

        # Execute the query with the provided values
        data = (id, FirstName, MiddleName, LastName, selected_course)
        cursor.execute(insert_query, data)

        # Commit the changes to the database and close the connection
        db_request.commit()
        db_request.close()

    def cancel_form(self):
        # Switch back to the main menu page
        self.controller.show_frame("MakerPage")

class LibraryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#EFEFEF')  # Set the background color for the entire page
        self.controller = controller

        # Create a colored square background frame to hold the labels and input fields
        form_frame = tk.Frame(self, bg='#5D1C1C',padx=50, pady=50)
        form_frame.pack(expand=True, fill=tk.BOTH)  # Allow the form_frame to fill available space

        # Create a label for the RegistrationPage
        request_label = tk.Label(form_frame, text="LIBRARY CARD INFORMATION FORM", font=('inter', 30, 'bold'), bg='#5D1C1C',
                                 fg='#FFFFFF')
        request_label.grid(row=0, column=1, columnspan=3, pady=18, sticky='N')

        note_label = tk.Label(form_frame,
                              text="Kindly provide the complete information needed in this online form.\n\n"
                                   "There is a 150 pesos ID fee to be paid at the Cashier's Office for the replacement.",
                              font=('inter', 15), bg='#5D1C1C', fg='#FFFFFF')
        note_label.grid(row=2, column=1, padx=50, pady=30, sticky='w')


        id_label = tk.Label(form_frame, text='ID Number:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        id_label.grid(row=4, column=0, padx=10, pady=15, sticky='e')

        self.id_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.id_entry.grid(row=4, column=1, padx=10, pady=15, sticky='w')

        # Create input fields for name, course, ID number, and QR code number
        FirstName_label = tk.Label(form_frame, text='First Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        FirstName_label.grid(row=5, column=0, padx=10, pady=15, sticky='e')

        self.FirstName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.FirstName_entry.grid(row=5, column=1, padx=10, pady=15, sticky='w')

        MiddleName_label = tk.Label(form_frame, text='Middle Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        MiddleName_label.grid(row=6, column=0, padx=10, pady=15, sticky='e')

        self.MiddleName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.MiddleName_entry.grid(row=6, column=1, padx=10, pady=15, sticky='w')

        LastName_label = tk.Label(form_frame, text='Last Name:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        LastName_label.grid(row=7, column=0, padx=10, pady=15, sticky='e')

        self.LastName_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
        self.LastName_entry.grid(row=7, column=1, padx=10, pady=15, sticky='w')

        course_label = tk.Label(form_frame, text='Course:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
        course_label.grid(row=8, column=0, padx=10, pady=15, sticky='e')

        # Create a Combobox for the "Course" field
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

        # Create the Proceed button, but set it to be disabled initially
        submit_button = tk.Button(form_frame, text='Submit', font=('inter', 18), command=self.show_confirmation, bg='#5D1C1C', fg='#FFFFFF')
        submit_button.grid(row=10, column=1, columnspan=1, padx=15,  pady=20)

        # Create the cancel button
        cancel_button = tk.Button(form_frame, text='Cancel', font=('inter', 18), command=self.cancel_form, bg='#5D1C1C', fg='#FFFFFF')
        cancel_button.grid(row=10, column=0, columnspan=2, padx=15, pady=20)

    def show_confirmation(self):
        # Retrieve the form data from the input fields
        # Gather the entered details from the input fields
        id = self.id_entry.get()
        FirstName = self.FirstName_entry.get()
        MiddleName = self.MiddleName_entry.get()
        LastName = self.LastName_entry.get()
        selected_course = self.course_var.get()

        # Clear the input fields
        self.id_entry.delete(0, tk.END)
        self.FirstName_entry.delete(0, tk.END)
        self.MiddleName_entry.delete(0, tk.END)
        self.LastName_entry.delete(0, tk.END)
        self.course_var.set("")

        # Create a message for the confirmation box
        confirmation_message = f"ID Number: {id}\nFirst Name: {FirstName}\nMiddle Name: {MiddleName}\nLast Name: {LastName}\nCourse: {selected_course}\nIs the information correct?"

        # Show a message box to confirm the entered details
        user_confirmation = messagebox.askyesno("Confirmation of Request", confirmation_message)

        if user_confirmation:
            # Save the data to the database
            self.save_data_to_database(id, FirstName, MiddleName, LastName, selected_course)

            # Show success message and navigate to the next page
            messagebox.showinfo("Success", "Data has been submitted.")
            self.controller.show_frame("MainMenu_Page")

    def save_data_to_database(self, id, FirstName, MiddleName, LastName, selected_course):
        # Establish a connection to the MySQL database
        db_request = mysql.connector.connect(
            host="localhost",
            user="root",
            password="030702",
            database="db_test"
        )
        cursor = db_request.cursor()

        # Define the SQL query to insert data into the database table
        insert_query = "INSERT INTO tbl_request (id_number, FirstName, MiddleName, LastName, course) VALUES (%s, %s, %s, %s, %s)"

        # Execute the query with the provided values
        data = (id, FirstName, MiddleName, LastName, selected_course)
        cursor.execute(insert_query, data)

        # Commit the changes to the database and close the connection
        db_request.commit()
        db_request.close()

    def cancel_form(self):
        # Switch back to the main menu page
        self.controller.show_frame("MakerPage")

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()