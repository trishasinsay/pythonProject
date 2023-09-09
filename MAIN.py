import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from tkinter import PhotoImage
import qrcode
import pygame.camera
import pygame.image
from PIL import Image
from pyzbar.pyzbar import decode

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MainMenu_Page, RequestPage, ValidationPage, MakerPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

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
                                       width=16, height= 2)

        # Place the button below the sub-heading label
        self.canvas.create_window(self.winfo_screenwidth() // 2 + 250, self.winfo_screenheight() // 2 + 215,
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

        # Load image for the button
        image1 = tk.PhotoImage(file='validation.png')
        image2 = tk.PhotoImage(file='requesting.png')
        image3 = tk.PhotoImage(file='maker.png')

        # Create the button with the background color and image on top
        button1 = tk.Button(self, image=image1, compound=tk.TOP, bg='#5D1C1C', height=300, width=330, command=self.on_button1_click, bd=0)
        button2 = tk.Button(self, image=image2, compound=tk.TOP, bg='#5D1C1C', height=300, width=330, command=self.on_button2_click, bd=0)
        button3 = tk.Button(self, image=image3, compound=tk.TOP, bg='#5D1C1C', height=300, width=330, command=self.on_button3_click, bd=0)

        # Set the image as button attribute to avoid garbage collection
        button1.image = image1
        button2.image = image2
        button3.image = image3

        # Add a label below the button
        label1 = tk.Label(self, text='ID VALIDATION', font=('inter', 25, 'bold'), background='#D8D8D8')
        label2 = tk.Label(self, text='ID REQUESTING', font=('inter', 25, 'bold'), background='#D8D8D8')
        label3 = tk.Label(self, text='ID MAKER', font=('inter', 25, 'bold'), background='#D8D8D8')

        # Grid layout for button and label
        button1.grid(row=0, column=0, padx=50, pady=90)
        label1.grid(row=1, column=0, padx=5, pady=2)

        button2.grid(row=0, column=1, padx=50, pady=90)
        label2.grid(row=1, column=1, padx=5, pady=2)

        button3.grid(row=0, column=2, padx=50, pady=90)
        label3.grid(row=1, column=2, padx=5, pady=2)

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

        form_url = "https://bit.ly/ID-Apply-TUPC"
        webbrowser.open(form_url)

    def on_button3_click(self):
        # Handle button 3 click event
        pass


class VideoWidget(tk.Canvas):
    def __init__(self, parent, on_qr_code_scanned):
        super().__init__(parent, width=640, height=480)
        self.camera = None
        self.after_id = None
        self.on_qr_code_scanned = on_qr_code_scanned
        self.start_camera()

    def start_camera(self):
        pygame.camera.init()
        camera_list = pygame.camera.list_cameras()
        if not camera_list:
            raise ValueError('No camera detected.')

        self.camera = pygame.camera.Camera(camera_list[0], (640, 480))
        self.camera.start()
        self.after(50, self.update_camera)

    def update_camera(self):
        if self.camera and self.camera.get_image():
            image = self.camera.get_image()
            image_data = pygame.image.tostring(image, 'RGB', False)
            img = Image.frombytes('RGB', (640, 480), image_data)
            photo = ImageTk.PhotoImage(img)

            self.create_image(0, 0, image=photo, anchor=tk.NW)
            self.photo = photo  # Store reference to avoid garbage collection

            # Check for QR codes in the camera feed
            qr_codes = decode(img)
            if qr_codes:
                qr_code_data = qr_codes[0].data.decode('utf-8')
                self.on_qr_code_scanned(qr_code_data)

        self.after_id = self.after(50, self.update_camera)

    def stop_camera(self):
        if self.after_id:
            self.after_cancel(self.after_id)

        if self.camera:
            self.camera.stop()
            self.camera = None
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

        # Define the background color for the scan label
        scan_label_bg_color = '#5D1C1C'

        self.scan_label = tk.Label(self, text='PLEASE SCAN YOUR ID', font=('inter', 30, 'bold'),
                                   fg='white', bg=scan_label_bg_color)  # Set the text color
        self.scan_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # Adjust the values of relx and rely

        # Create a button to start the QR scanner
        self.self_scan_button = tk.Button(self, text="Start Scan", command=self.on_start_qr_scan)
        self.self_scan_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Create a button to start the QR scanner
        self.self_scan_button = tk.Button(self, text="Start Scan", command=self.start_qr_scan)
        self.self_scan_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

class RequestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class MakerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

if __name__ == "__main__":
    app = SampleApp()
    main_menu_frame = MainMenu_Page(app, app)
    main_menu_frame.pack(fill='both', expand=True)
    app.mainloop()

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
        self.camera_preview = CameraPreview(self, width=640, height=480)
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


# Create labels and input fields for other information using grid layout
        email_label = tk.Label(self, text="Email:")
        email_label.grid(row=1, column=0, padx=10, pady=5)
        email_entry = tk.Entry(self)
        email_entry.grid(row=1, column=1, padx=10, pady=5)

        id_number_label = tk.Label(self, text="ID Number:")
        id_number_label.grid(row=2, column=0, padx=10, pady=5)
        id_number_entry = tk.Entry(self)
        id_number_entry.grid(row=2, column=1, padx=10, pady=5)

        # Dropdown for type of request selection
        request_type_var = tk.StringVar()
        request_type_label = tk.Label(self, text="Type of Request", font=('inter', 12))
        request_type_label.pack(pady=5)
        request_type_combobox = ttk.Combobox(self, textvariable=request_type_var,
                                             values=["REPLACEMENT (for old students with lost ID)", "REPLACEMENT (for old students with damaged ID that needs replacement)", "UNCLAIMED"], font=('inter', 12),
                                             state="readonly")
        request_type_combobox.set("Select Type of Request")
        request_type_combobox.pack(pady=5)

        last_name_label = tk.Label(self, text="Last Name:")
        last_name_label.grid(row=3, column=0, padx=10, pady=5)
        last_name_entry = tk.Entry(self)
        last_name_entry.grid(row=3, column=1, padx=10, pady=5)

        first_name_label = tk.Label(self, font=('inter', 12), width=30)
        first_name_label.grid(row=3, column=0, padx=10, pady=5)
        last_name_entry = tk.Entry(self)
        last_name_entry.grid(row=3, column=1, padx=10, pady=5)

        middle_initial_entry = tk.Entry(self, font=('inter', 12), width=30)
        middle_initial_entry.insert(0, "Middle Initial")
        middle_initial_entry.pack(pady=10)

        contact_number_entry = tk.Entry(self, font=('inter', 12), width=30)
        contact_number_entry.insert(0, "Contact Number")
        contact_number_entry.pack(pady=10)

        # Dropdown for program selection
        program_var = tk.StringVar()
        program_label = tk.Label(self, text="Program", font=('inter', 12))
        program_label.pack(pady=5)
        program_combobox = ttk.Combobox(self, textvariable=program_var,
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
                                        font=('inter', 12), state="readonly")
        program_combobox.set("Select Program")
        program_combobox.pack(pady=5)

        emergency_contact_name_entry = tk.Entry(self, font=('inter', 12), width=30)
        emergency_contact_name_entry.insert(0, "Emergency Contact Name")
        emergency_contact_name_entry.pack(pady=10)

        emergency_contact_number_entry = tk.Entry(self, font=('inter', 12), width=30)
        emergency_contact_number_entry.insert(0, "Emergency Contact Number")
        emergency_contact_number_entry.pack(pady=10)

        address_entry = tk.Entry(self, font=('inter', 12), width=30)
        address_entry.insert(0, "Address")
        address_entry.pack(pady=10)
        # Add other fields here using grid layout

        # Create a style object
        style = ttk.Style()

        # Configure the 'TEntry' element of the style to have rounded corners
        style.configure('TEntry', borderwidth=0, bordercolor='#D8D8D8', relief=tk.FLAT, background='#FFFFFF',
                        foreground='#000000', fieldbackground='#FFFFFF', focuscolor='#00a8ff', focusthickness=2,
                        focusthicknessfor=0)

        # Apply the style to all Entry widgets
        for entry in self.winfo_children():
            if isinstance(entry, tk.Entry):
                entry.config(style='TEntry')
                entry.bind("<FocusIn>", self.clear_placeholder)

    def clear_placeholder(self, event):
        # Function to clear the placeholder text when the entry gains focus
        widget = event.widget
        current_text = widget.get()
        placeholder_text = widget.getPlaceholder()
        if current_text == placeholder_text:
            widget.delete(0, tk.END)


        # Button to submit the form (you can add a command to handle form submission)
        submit_button = tk.Button(self, text="Submit", font=('inter', 12), bg='#5D1C1C', fg='white', command=self.submit_form)
        submit_button.pack(pady=20)

    def submit_form(self):
        # Implement your code to handle form submission here
        # You can access the form data using the entry fields and comboboxes, e.g., email_entry.get(), id_number_entry.get(), program_var.get(), request_type_var.get(), etc.
        # For now, let's just print the form data as an example
        print("Email:", email_entry.get())
        print("ID Number:", id_number_entry.get())
        print("Last Name:", last_name_entry.get())
        print("First Name:", first_name_entry.get())
        print("Middle Initial:", middle_initial_entry.get())
        print("Contact Number:", contact_number_entry.get())
        print("Emergency Contact Name:", emergency_contact_name_entry.get())
        print("Emergency Contact Number:", emergency_contact_number_entry.get())
        print("Address:", address_entry.get())
        print("Program:", program_var.get())
        print("Type of Request:", request_type_var.get())



        # After handling the form submission, you can do any further processing or navigate to other pages
        # For example, you can show a success message or navigate back to the main menu
        self.controller.show_frame("MainMenuPage")

        class MatchingPage(tk.Frame):
            def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                self.controller = controller

                # Create a canvas that covers the entire frame with a background color
                self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight(),
                                        bg='#5D1C1C')
                self.canvas.pack()

                sub_heading_label = 'Please scan your Certificate of Registration'
                sub_heading_label = self.canvas.create_text(self.winfo_screenwidth() // 2,
                                                            self.winfo_screenheight() // 3,
                                                            text=sub_heading_label, font=('inter', 17),
                                                            fill='White')  # Set the text color
                self.canvas.coords(sub_heading_label, self.winfo_screenwidth() // 2,
                                   self.winfo_screenheight() // 4 - 130)

                # Create a label for the text extraction results
                self.text_result_label = tk.Label(self, text='', font=('inter', 14), fg='white', bg='#5D1C1C')
                self.text_result_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

                # Define the background color for the scan button
                scan_button_bg_color = '#5D1C1C'

                # Create Scan button with background color
                self.scan_button = tk.Button(self, text='TAP TO SCAN YOUR COR', font=('inter', 16, 'bold'), fg='white',
                                             bg=scan_button_bg_color,
                                             width=28, command=self.start_qr_scan_thread)
                self.scan_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)  # Adjust the values of relx and rely

                # Create the camera preview label
                self.camera_preview_label = tk.Label(self, width=950, height=80, bg='black')
                self.camera_preview_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=750, height=450)

                # Define the Region of Interest (ROI) coordinates as a fraction of the frame size
                roi_top_left = (0.1, 0.3)  # (relx, rely)
                roi_bottom_right = (0.9, 0.7)  # (relx, rely)

                # Convert relative coordinates to absolute coordinates in pixels
                frame_width = self.winfo_screenwidth()
                frame_height = self.winfo_screenheight()
                x1 = int(roi_top_left[0] * frame_width)
                y1 = int(roi_top_left[1] * frame_height)
                x2 = int(roi_bottom_right[0] * frame_width)
                y2 = int(roi_bottom_right[1] * frame_height)

                self.roi_coordinates = (x1, y1, x2, y2)

                # Initialize variables to hold the camera capture and thread state
                self.cap = None
                self.thread_running = False

            def start_qr_scan_thread(self):
                # Create a new thread to run the QR code scanning process and camera preview
                qr_scan_thread = threading.Thread(target=self.start_qr_scan)
                qr_scan_thread.start()

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
                self.camera_preview = CameraPreview(self, width=640, height=480)
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

        class RequestPage(tk.Frame):
            def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent, bg='#EFEFEF')  # Set the background color for the entire page
                self.controller = controller

                # Create the form frame
                # Create a colored square background frame to hold the labels and input fields
                form_frame = tk.Frame(self, bg='#5D1C1C', width=700, height=900, padx=50, pady=100)
                form_frame.pack(expand=True, fill=tk.BOTH)  # Allow the form_frame to fill available space

                # Center the form_frame within the window
                form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

                # Create a label for the RegistrationPage
                request_label = tk.Label(self, text="REQUEST FORM", font=('inter', 30, 'bold'), bg='#5D1C1C',
                                         fg='#FFFFFF')
                request_label.grid(row=0, column=0, columnspan=3, pady=20, sticky='N')

                note_label = tk.Label(self,
                                      text="Kindly provide the complete information needed in this online form.\n\n"
                                           "There is a 150 pesos ID fee to be paid at the Cashier's Office for the replacement.",
                                      font=('inter', 15), bg='#5D1C1C', fg='#FFFFFF')
                note_label.grid(row=2, column=1, padx=10, pady=30, sticky='e')

                # Create a label for the "Date of Request" field
                date_label = tk.Label(self, text="Date of Request:", font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
                date_label.grid(row=3, column=0, padx=(20, 2), pady=15, sticky="w")

                # Create a DateEntry widget for the date input
                self.date_of_request_var = DateEntry(self, font=('inter', 15), width=25)  # Adjust the width here))
                self.date_of_request_var.grid(row=3, column=1, padx=(10, 2), pady=15, sticky="w")

                id_number_label = tk.Label(self, text='ID Number:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
                id_number_label.grid(row=3, column=1, padx=(450, 2), pady=15, sticky='w')

                self.id_number_var = tk.Entry(self, font=('inter', 15), width=20)
                self.id_number_var.grid(row=3, column=1, padx=(580, 2), pady=15, sticky='w')

                # Create input fields for name, course, ID number, and QR code number
                fname_label = tk.Label(self, text='FirstName:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
                fname_label.grid(row=4, column=0, padx=(30, 2), pady=15, sticky='e')

                self.fname_var = tk.Entry(self, font=('inter', 14), width=30)  # Adjust the width here
                self.fname_var.grid(row=4, column=1, padx=(2, 2), pady=25, sticky='w')

                mInitial_label = tk.Label(self, text='MiddleName:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
                mInitial_label.grid(row=4, column=1, padx=(360), pady=15, sticky='w')

                self.mInitial_var = tk.Entry(self, font=('inter', 14), width=18)  # Adjust the width here
                self.mInitial_var.grid(row=4, column=1, padx=(510, 2), pady=15, sticky='w')

                lname_label = tk.Label(self, text='LastName:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
                lname_label.grid(row=4, column=1, padx=(720, 2), pady=15, sticky='W')

                self.lname_var = tk.Entry(self, font=('inter', 14), width=18)  # Adjust the width here
                self.lname_var.grid(row=4, column=1, padx=(850, 2), pady=15, sticky='w')

                course_label = tk.Label(self, text='Course:', font=('inter', 18), bg='#5D1C1C', fg='#FFFFFF')
                course_label.grid(row=7, column=0, padx=10, pady=15, sticky='e')

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
                                               font=('inter', 12), state="readonly", width=110)
                course_combobox.grid(row=7, column=1, padx=10, pady=15, sticky="w")

                # Create the Proceed button, but set it to be disabled initially
                submit_button = tk.Button(self, text='Submit', font=('inter', 18), command=self.show_confirmation,
                                          bg='#5D1C1C', fg='#FFFFFF')
                submit_button.grid(row=9, column=1, columnspan=1, pady=20)

                # Create the cancel button
                cancel_button = tk.Button(self, text='Cancel', font=('inter', 18), bg='#5D1C1C',
                                          command=self.cancel_form,
                                          fg='#FFFFFF')
                cancel_button.grid(row=9, column=0, columnspan=2, pady=20)

            def show_confirmation(self):
                # Gather the entered details from the input fields
                date_of_request = self.date_of_request_var.get()
                id_number = self.id_number_var.get()
                fname = self.fname_var.get()
                mInitial = self.mInitial_var.get()
                lname = self.lname_var.get()
                selected_course = self.course_var.get()

                selected_course = self.course_var.get()  # Get the selected course from the StringVar

                # Clear the input fields
                self.date_of_request_var.delete(0, tk.END)
                self.id_number_var.delete(0, tk.END)
                self.fname_var.delete(0, tk.END)
                self.mInitial_var.delete(0, tk.END)
                self.lname_var.delete(0, tk.END)
                self.course_var.set("")

                # Show a message box to confirm the entered details
                user_confirmation = messagebox.askyesno("Confirmation of Request", confirmation_message)

                # Create a message for the confirmation box
                confirmation_message = f"Date of Request: {date_of_request}\nID Number: {id_number}\nFirstName: {fname}\nMiddleName: {mInitial}\nLastName: {lname}\nCourse: {selected_course}\nIs the information correct?"

                # Show a message box to confirm the entered details
                user_confirmation = messagebox.askyesno("Confirmation", confirmation_message)

                if user_confirmation:
                    # Save the data to the database
                    self.save_data_to_database(date_of_request, id_number, fname, mInitial, lname, selected_course)

                    # Show success message and navigate to the next page
                    messagebox.showinfo("Success", "Data has been submitted.")
                    self.controller.show_frame("MainMenu_Page")

            def save_data_to_database(self, date_of_request, id_number, fname, mInitial, lname, selected_course):
                # Establish a connection to the MySQL database
                db_request = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="030702",
                    database="db_request"
                )
                cursor = db_request.cursor()

                # Define the SQL query to insert data into the database table
                insert_query = "INSERT INTO tbl_request (date_of_request, id_number, fname, mInitial, lname, course) VALUES (%s, %s, %s, %s, %s, %s)"

                # Execute the query with the provided values
                data = (date_of_request, id_number, fname, mInitial, lname, selected_course)
                cursor.execute(insert_query, data)

                # Commit the changes to the database and close the connection
                db_request.commit()
                db_request.close()

            def cancel_form(self):
                # Switch back to the main menu page
                self.controller.show_frame("MainMenu_Page")

                MiddleInitial_label = tk.Label(form_frame, text='Middle Name:', font=('inter', 18), bg='#5D1C1C',
                                               fg='#FFFFFF')
                MiddleInitial_label.grid(row=6, column=0, padx=10, pady=15, sticky='e')

                self.MiddleInitial_entry = tk.Entry(form_frame, font=('inter', 14), width=25)
                self.MiddleInitial_entry.grid(row=6, column=1, padx=10, pady=15, sticky='w')