import threading
import tkinter as tk
import tkinter as ttk
from tkinter import Tk, Canvas  # Import the Canvas class
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
import qrcode
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
        for F in (StartPage, MainMenu_Page, RequestPage, MakerPage, ValidationPage):
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
        self.bg_image = Image.open('Group 48.png')
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
        image_path = 'arrow.png'  # Replace with the path to your image
        if os.path.exists(image_path):
            image = Image.open(image_path)

            # Calculate the position of the image in the upper right corner
            image_width, image_height = image.size
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            image_x = screen_width - 150
            image_y = 770

            # Create a PhotoImage object from the cropped image
            image = ImageTk.PhotoImage(image)

            # Create a label to display the image with a transparent background
            image_label = tk.Label(self, image=image, bg="#151716")
            image_label.place(x=image_x, y=image_y)

            # Keep a reference to the image to prevent it from being garbage collected
            image_label.image = image
        else:
            print(f"Image file not found: {image_path}")

        # Load the image
        image_path = 'banner.png'  # Replace with the path to your image
        if os.path.exists(image_path):
            image = Image.open(image_path)

            # Calculate the position of the image in the upper right corner
            image_width, image_height = image.size
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            image_x = screen_width // 8 - 180
            image_y =80

            # Create a PhotoImage object from the cropped image
            image = ImageTk.PhotoImage(image)

            # Create a label to display the image with a transparent background
            image_label = tk.Label(self, image=image, bg="#D0CFD2")
            image_label.place(x=image_x, y=image_y)

            # Keep a reference to the image to prevent it from being garbage collected
            image_label.image = image
        else:
            print(f"Image file not found: {image_path}")

        # Add header text inside the rectangle
        header_text1 = self.canvas.create_text(screen_width // 2+5, 37,
                                                text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE",
                                                fill="black",
                                                font=("Cambria", 26))

        header_text = self.canvas.create_text(950, 350, text="WELCOME", fill="#862C3C",
                                         font=("Times New Roman", 160, 'bold'))
        header =self.canvas.create_text(948, 348, text="WELCOME", fill="white", font=("Times New Roman", 160, 'bold'))

        # Add subheader text below the header text
        subheader_text = self.canvas.create_text(screen_width // 2, 550, text="T U P C I A N S !", fill="white",
                                                     font=('Anonymous Pro', 70, 'bold', "italic"))
        sub_header = self.canvas.create_text(screen_width // 2-2, 548, text="T U P C I A N S !", fill="#862C3C", font=('Anonymous Pro', 70, 'bold', "italic"))

        # Add another text element below the subheader text
        note_text = self.canvas.create_text(screen_width // 3 - 80, 900,
                                            text=" Welcome to our ID Maker Kiosk, students, faculty, and alumni! We are thrilled to\n offer this convenient service to help you obtain your IDs. Whether you need a new\n or a replacement ID, we are here to assist you.",
                                            fill="white",
                                            font=("Times New Roman", 23, "italic"))

        # Add clickable text button
        clickable_text = self.canvas.create_text(screen_width // 1.3 + 30, 780, text="Get Started", fill="white",
                                                 font=("Times New Roman", 80, 'italic'))
        self.canvas.tag_bind(clickable_text, "<Button-1>", self.on_clickable_text_click)

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

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill="both")

        self.canvas.config(borderwidth=0, highlightthickness=0)

        # Load the background image using PIL
        self.bg_image1 = Image.open('Group 47.png')
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
        width_scale = screen_width / self.bg_image1.width
        height_scale = screen_height / self.bg_image1.height

        # Resize the background image
        resized_bg_image1 = self.bg_image1.resize((screen_width, screen_height))

        # Create a PhotoImage object from the resized image
        self.bg_photo1 = ImageTk.PhotoImage(resized_bg_image1)

        # Update the canvas image
        self.canvas.create_image(0, 0, image=self.bg_photo1, anchor=tk.NW)

        # Load image for the button
        image1 = Image.open('validation.png')
        image2 = Image.open('requesting.png')
        image3 = Image.open('maker.png')
        image4 = Image.open('back.png')


        # Create PhotoImage objects and assign them to instance variables
        self.image1 = ImageTk.PhotoImage(image1)
        self.image2 = ImageTk.PhotoImage(image2)
        self.image3 = ImageTk.PhotoImage(image3)
        self.image4 = ImageTk.PhotoImage(image4)

        # Add a text label
        # Add header text inside the rectangle
        header_text1 = self.canvas.create_text(screen_width // 2 + 5, 37,
                                               text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE",
                                               fill="black", font=("Cambria", 26))

        header = self.canvas.create_text(screen_width // 2, 230, text="M A I N  M E N U", fill="black", font=("Cambria", 100, 'bold'))
        header2 = self.canvas.create_text(screen_width // 2 -4, 228, text="M A I N  M E N U", fill="white", font=("Cambria", 100, 'bold'))

        req_text = self.canvas.create_text(360, 810, text="REQUEST", fill="#5C1C1C", font=("Cambria", 30))

        maker_text = self.canvas.create_text(960, 810, text="ID MAKER", fill="#5C1C1C", font=("Cambria", 30))

        validation_text = self.canvas.create_text(1565, 810, text="VALIDATION", fill="#5C1C1C", font=("Cambria", 30))

        # Create buttons with images
        req_button = tk.Button(self, image=self.image2, compound=tk.TOP, bg="black", width=270, height=250, bd=0, command=self.on_button1_click)
        self.canvas.create_window(235, 455, window=req_button, anchor="nw")

        maker_button = tk.Button(self, image=self.image3, compound=tk.TOP, bg="black", width=270, height=250, bd=0,  command=self.on_button2_click)
        self.canvas.create_window(825, 455, window=maker_button, anchor="nw")

        valid_button = tk.Button(self, image=self.image1, compound=tk.TOP, bg="black", width=270, height=250, bd=0, command=self.on_button3_click)
        self.canvas.create_window(1415, 455, window=valid_button, anchor="nw")

        back_button = tk.Button(self, image=self.image4, compound=tk.LEFT, bg="#862c3c", width=80, height=80, bd=0,  command=self.on_back_button_click)
        self.canvas.create_window(20, 95, window=back_button, anchor="nw")



    def on_button1_click(self):
        if self.button_click_in_progress:
            return  # Return without taking action
        self.button_click_in_progress = True
        self.controller.show_frame('RequestPage')

        # Set the flag back to False when the action is complete
        self.button_click_in_progress = False

    def on_button2_click(self):
        if self.button_click_in_progress:
            return
        self.button_click_in_progress = True
        self.controller.show_frame('MakerPage')
        self.button_click_in_progress = False

    def on_button3_click(self):
        if self.button_click_in_progress:
            return
        self.button_click_in_progress = True
        self.controller.show_frame('ValidationPage')

        self.button_click_in_progress = False

    def on_back_button_click(self):
        # Switch back to the StartPage
        self.controller.show_frame('StartPage')


class RequestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#5D1C1C")
        self.controller = controller

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill="both")

        self.canvas.config(borderwidth=0, highlightthickness=0)

        # Load the background image using PIL
        self.bg_image = Image.open('request.png')
        self.update_background()


        # Bind the canvas to the window resizing
        self.bind("<Configure>", self.on_resize)

        self.validate_fields()

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
        header_rectangle = self.canvas.create_rectangle(0, 0, screen_width, 3, fill="black")

        # Add header text inside the rectangle
        header_text = self.canvas.create_text(screen_width // 2 + 30, 35, text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE", fill="white",
                                              font=("Cambria", 27))

        # Load the image you want to display
        image_path = 'tup.jpg'  # Replace with your image file path
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image.thumbnail((120, 60))  # Adjust the size as needed
            image = ImageTk.PhotoImage(image)

            # Create a label to display the image
            image_label = tk.Label(self, image=image, bg="white", borderwidth=0, highlightthickness=0)
            image_label.photo = image
            image_label.place(x=420, y=10)  # Adjust the position as needed


        # Add header text below the header rectangle
        header_text_below = self.canvas.create_text(screen_width // 2, 120, text="R E Q U E S T  F O R M", fill="black",
                                                    font=('cambria', 40, 'bold'))
        header_text_below = self.canvas.create_text(screen_width // 2 - 4, 118, text="R E Q U E S T  F O R M", fill="white",
                                                    font=('cambria', 40, 'bold'))

        # Add header text below the header rectangle
        notetext_below = self.canvas.create_text(screen_width // 2 + 20, 170, text="Kindly provide the complete information needed in this online form.", fill="white",
                                                    font=('IBM Plex Mono', 17))

        # Add header text below the header rectangle
        note_text_below = self.canvas.create_text(screen_width // 2 + 20, 206, text="There is a 150 pesos ID fee to be paid at the Cashier's Office for the replacement.",
                                                 fill="white", font=('IBM Plex Mono', 17))

        # Create a label for the user's role in university
        role_label = self.canvas.create_text(screen_width // 2.5 - 450, 260, text="Role in University:",
                                             font=("Cambria", 20, "bold"), fill='white')

        self.role_var = tk.StringVar()
        role_combobox = ttk.Combobox(self, textvariable=self.role_var,
                                     values=["Student", "Faculty", "Alumni"],
                                     font=("Cambria", 16), state="readonly")
        role_combobox.place(x=500, y=250, width=1100, height=35)
        role_combobox.set("Select your Role in University")  # Set the default value


        # Create a label for the user's email
        email_label = self.canvas.create_text(screen_width // 2.55 - 430, 330, text="GSFE Email / Email:", font=("Cambria", 20, "bold"),
                                              fill='white')

        # Create an entry widget for the user's email
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(self, font=("Cambria", 16))
        self.email_entry.place(x=500, y=310, width=1100, height=35)

        # Bind a click event to the email entry to show the system keyboard
        self.email_entry.bind("<Button-1>", self.show_system_keyboard)

        # Create a label for the student ID
        id_number_label = self.canvas.create_text(screen_width // 2.65 - 450, 390, text="Student ID:",
                                                  font=("Cambria", 20, "bold"),
                                                  fill='white')

        # Create an entry widget for the student ID
        self.id_number_var = tk.StringVar()
        self.id_number_entry = tk.Entry(self, font=("Cambria", 16))
        self.id_number_entry.place(x=500, y=370, width=1100, height=35)

        self.id_number_entry.bind("<Button-1>", self.show_system_keyboard)

        # Create a label for the student request
        request_type_label = self.canvas.create_text(screen_width // 2.5 - 445, 455, text="Type of ID Request:",
                                                     font=("Cambria", 20, "bold"), fill='white')

        self.type_var = tk.StringVar()
        request_type_combobox = ttk.Combobox(self, textvariable=self.type_var,
                                             values=[
                                                 "REPLACEMENT(For old students with lost ID)",
                                                 "REPLACEMENT(For old students with damaged ID that needs replacement)",
                                                 "New ID"],
                                             font=("Cambria", 16), state="readonly")
        request_type_combobox.place(x=500, y=440, width=1100, height=35)
        request_type_combobox.set("Select Type of ID Request")

        # Create a label for the reason
        reason_label = self.canvas.create_text(screen_width // 2.6 - 440, 525, text="Specify Reason:", font=("Cambria", 20, "bold"),
                                               fill='white')

        self.reason_var = tk.StringVar()
        self.reason_entry = tk.Entry(self, font=("Cambria", 16))
        self.reason_entry.place(x=500, y=510, width=1100, height=35)

        # Create a label for the student lastname
        lastname_label = self.canvas.create_text(screen_width // 2.65 - 450, 595, text="Last Name:", font=("Cambria", 20, "bold"),
                                                 fill='white')

        # Create an entry widget for the student lastname
        self.lastname_var = tk.StringVar()
        self.lastname_entry = tk.Entry(self, font=("Cambria", 16))
        self.lastname_entry.place(x=500, y=580, width=1100, height=35)

        self.lastname_entry.bind("<Button-1>", self.show_system_keyboard)

        # Create a label for the student firstname
        firstname_label = self.canvas.create_text(screen_width // 2.65 - 450, 665, text="First Name:",
                                                  font=("Cambria", 20, "bold"),
                                                  fill='white')

        # Create an entry widget for the student firstname
        self.firstname_var = tk.StringVar()
        self.firstname_entry = tk.Entry(self, font=("Cambria", 16))
        self.firstname_entry.place(x=500, y=650, width=1100, height=35)

        self.firstname_entry.bind("<Button-1>", self.show_system_keyboard)

        # Create a label for the student middle name
        middlename_label = self.canvas.create_text(screen_width // 2.60 - 450, 725, text="Middle Name:",
                                                   font=("Cambria", 20, "bold"),
                                                   fill='white')

        # Create an entry widget for the student middle name
        self.middlename_var = tk.StringVar()
        self.middlename_entry = tk.Entry(self, font=("Cambria", 16))
        self.middlename_entry.place(x=500, y=710, width=1100, height=35)

        self.middlename_entry.bind("<Button-1>", self.show_system_keyboard)

        # Create a label for the student contact number
        contact_label = self.canvas.create_text(screen_width // 2.65 - 450, 795, text="Contact No.:",
                                                font=("Cambria", 20, "bold"),
                                                fill='white')

        # Create an entry widget for the student contact number
        self.contact_var = tk.StringVar()
        self.contact_entry = tk.Entry(self, font=("Cambria", 16))
        self.contact_entry.place(x=500, y=780, width=1100, height=35)

        self.contact_entry.bind("<Button-1>", self.show_system_keyboard)

        # Create a label for the student program or course
        program_label = self.canvas.create_text(screen_width // 2.69 - 450, 860, text="Program:", font=("Cambria", 20, "bold"),
                                                fill='white')

        self.course_var = tk.StringVar()
        course_combobox = ttk.Combobox(self, textvariable=self.course_var,
                                       values=[
                                           "BSCE", "BSEE", 'BSME', 'BSIE-ICT', "BSIE-HE", "BSIE-IA",
                                           "BTTE-CP",
                                           "BTTE-EI", "BTTE-AU", "BTTE-HVACT", "BTTE-E", "BGT-AT",
                                           "BET-CT",
                                           "BET-ET", "BET-ESET", "BET-COET", "BET-MT", "BET-PPT", "BET-AT"
                                       ],
                                       font=("Cambria", 16), state="readonly")
        course_combobox.place(x=500, y=840, width=1100, height=35)
        course_combobox.set("Select your Program")

        # Create the "Clear" button
        self.clear_button = tk.Button(self, text="Clear", font=("IBM Plex Mono", 18, 'bold'), command=self.clear_form,
                                  width=14)
        self.clear_button.place(relx=0.06, rely=0.96, anchor="sw")

        # Create the "Submit" button
        self.submit_button = tk.Button(self, text="Submit", font=("IBM Plex Mono", 18, 'bold'), command=self.submit_form, width=14)
        self.submit_button.place(relx=0.83, rely=0.95, anchor="se")

        # Create the "Cancel" button
        self.cancel_button = tk.Button(self, text="Cancel", font=("IBM Plex Mono", 18, 'bold'), command=self.cancel_form, width=14)
        self.cancel_button.place(relx=0.96, rely=0.95, anchor="se")

        # Bind the validation function to the variables
        self.role_var.trace_add("write", self.validate_fields)
        self.email_var.trace_add("write", self.validate_fields)
        self.id_number_var.trace_add("write", self.validate_fields)
        self.type_var.trace_add("write", self.validate_fields)
        self.reason_var.trace_add("write", self.validate_fields)
        self.lastname_var.trace_add("write", self.validate_fields)
        self.firstname_var.trace_add("write", self.validate_fields)
        self.middlename_var.trace_add("write", self.validate_fields)
        self.contact_var.trace_add("write", self.validate_fields)
        self.course_var.trace_add("write", self.validate_fields)

        # Call the validate_fields method to initially enable or disable the "Submit" button
        self.validate_fields()

    def show_system_keyboard(self, event):
        # Use the 'subprocess' module to execute a command to show the system keyboard
        subprocess.run(["cmd", "/c", "start", "osk.exe"])

    def validate_fields(self, *args):
        # Check if all required fields are non-empty
        if all([(self.role_var.get() != 'Select your Role in University' and self.email_entry.get() and self.id_number_entry.get() and self.type_var.get() != 'Select Type of ID Request' and
                        self.reason_entry.get() and self.lastname_entry.get() and self.firstname_entry.get() and self.middlename_entry.get() and self.contact_entry.get() and
                        self.course_var.get() != 'Select your Program')]):
            # Enable the "Submit" button if all fields are filled
            self.submit_button.config(state=tk.NORMAL)
        else:
            # Disable the "Submit" button if any field is empty
            self.submit_button.config(state=tk.DISABLED)


    def submit_form(self):
        selected_role = self.role_var.get()
        selected_request =self.type_var.get()
        reason = self.reason_entry.get()
        email = self.email_entry.get()
        id_number = self.id_number_entry.get()
        lastname = self.lastname_entry.get()
        firstname = self.firstname_entry.get()
        middlename = self.middlename_entry.get()
        contact = self.contact_entry.get()
        selected_course = self.course_var.get()

        # Check the length of the contact number
        if contact and (len(contact) < 11 or len(contact) > 11):
            messagebox.showerror("Invalid Contact Number", "Contact number should be 11 digits long.")
        else:
            # Create a message for the confirmation box
            confirmation_message = f"Role in University: {selected_role}\nType of ID Request: {selected_request}\nReason: {reason}\nEmail: {email}\nStudent ID Number: {id_number}\nLast Name: {lastname}\nFirst Name: {firstname}\nMiddle Name: {middlename}\nContact No.: {contact}\nProgram: {selected_course}\nIs the information correct?"

            # Show a message box to confirm the entered details
            user_confirmation = messagebox.askyesno("Confirmation of Request", confirmation_message)

            if user_confirmation:
                # Save the data to the database
                self.save_data_to_database(selected_role, selected_request, reason, email, id_number, lastname,
                                           firstname, middlename, contact, selected_course)

                # Show success message and navigate to the next page
                messagebox.showinfo("Success", "Data has been submitted.")
                self.controller.show_frame("MainMenu_Page")

                # Clear the input fields
                self.role_var.set('Select your Role in University')
                self.type_var.set("Select your Type of ID Request")
                self.reason_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                self.id_number_entry.delete(0, tk.END)
                self.lastname_entry.delete(0, tk.END)
                self.firstname_entry.delete(0, tk.END)
                self.middlename_entry.delete(0, tk.END)
                self.contact_entry.delete(0, tk.END)
                self.course_var.set("Select your Program")

            else:
                return None

    def save_data_to_database(self, Role, Email, StudentID, Request, Reason, LastName, FirstName, MiddleName, ContactNo, Program):
        # Establish a connection to the MySQL database
        db_request = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kiosk1234",
            port=3306,
            database="kiosk_db"
        )
        cursor = db_request.cursor()

        # Define the SQL query to insert data into the database table
        insert_query = "INSERT INTO tb_request (Role, Email, StudentID, Request, Reason, LastName, FirstName, MiddleName, ContactNo, Program) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Execute the query with the provided values
        data = (Role, Email, StudentID, Request, Reason, LastName, FirstName, MiddleName, ContactNo, Program)
        cursor.execute(insert_query, data)

        # Commit the changes to the database and close the connection
        db_request.commit()
        db_request.close()

    def cancel_form(self):
        # Switch back to the main menu page
        self.controller.show_frame("MainMenu_Page")

    def clear_form(self):
        # Clear the input fields
        self.role_var.set('Select your Role in University')
        self.type_var.set("Select your Type of ID Request")
        self.reason_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.id_number_entry.delete(0, tk.END)
        self.lastname_entry.delete(0, tk.END)
        self.firstname_entry.delete(0, tk.END)
        self.middlename_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.course_var.set("Select your Program")

class MakerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill="both")

        self.canvas.config(borderwidth=0, highlightthickness=0)

        # Load the background image using PIL
        self.bg_image = Image.open('Frame 14.png')
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

        # Add header text inside the rectangle
        header_text1 = self.canvas.create_text(screen_width // 2 + 5, 37,
                                               text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE",
                                               fill="black", font=("Cambria", 26))

        header_text = self.canvas.create_text(950, 350, text="WELCOME", fill="#862C3C",
                                              font=("Times New Roman", 160, 'bold'))
        header = self.canvas.create_text(948, 348, text="WELCOME", fill="white", font=("Times New Roman", 160, 'bold'))

        # Add subheader text below the header text
        subheader_text = self.canvas.create_text(screen_width // 2, 550, text="T U P C I A N S !", fill="white",
                                                 font=('Anonymous Pro', 70, 'bold', "italic"))
        sub_header = self.canvas.create_text(screen_width // 2 - 2, 548, text="T U P C I A N S !", fill="#862C3C",
                                      font=('Anonymous Pro', 70, 'bold', "italic"))

        # Add subheader text below the header text
        note = self.canvas.create_text(screen_width // 2, 650, text="Please enter OTP Code", fill="black",
                                                 font=('Anonymous Pro', 30, 'bold', "italic"))
        note = self.canvas.create_text(screen_width // 2 - 2, 658, text="Please enter OTP Code", fill="white",
                                             font=('Anonymous Pro', 30, 'bold', "italic"))

        submit = tk.Button(self, text="SUBMIT", compound=tk.LEFT, bg="#CECFD3", width=25,font=("Times New Roman", 35, 'italic'), command=self.validate_and_submit)
        self.canvas.create_window(960, 950, window=submit, anchor="s")

        backbutton_image = Image.open('back.png')
        self.backbutton_image = ImageTk.PhotoImage(backbutton_image)

        back_button = tk.Button(self, image=self.backbutton_image, compound=tk.LEFT, bg="#CECFD3", width=80, height=80, bd=0,
                                command=self.on_back_button_click)
        self.canvas.create_window(20, 95, window=back_button, anchor="nw")

        # Add an entry widget
        self.entry_box_var = tk.StringVar()
        entry_box = tk.Entry(self, textvariable=self.entry_box_var, font=("cambria", 40, 'bold'), bg='#D9D9D9', width=34, bd=0,
                                fg='black', justify="center")
        self.canvas.create_window(430, 720, window=entry_box, anchor="nw")

    # Function to execute when the button is clicked
    def on_back_button_click(self):
        self.on_get_started_button_click()

    def on_link_text_click(self, event):
        self.on_get_started_button_click()

    def on_get_started_button_click(self):
        # Switch to the main menu with three buttons
        main_menu_page_frame = MainMenu_Page(self.controller, self.controller)
        main_menu_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('MainMenu_Page')

    def validate_and_submit(self):
        # Get the text from the entry widget
        input_text = self.entry_box_var.get()

        # Define a regular expression pattern to match the format "A-XXXXXX"
        pattern_alumni = r'^[A]-\d{6}$'
        pattern_student = r'^[S]-\d{6}$'
        pattern_faculty = r'^[F]-\d{6}$'

        if re.match(pattern_alumni, input_text):
            # The input matches the alumni format, open alumni.py
            subprocess.Popen(['python', 'alumni.py'])
            self.entry_var.set('')
        elif re.match(pattern_student, input_text):
            # The input matches the student format, open student.py
            subprocess.Popen(['python', 'id_front.py'])
            self.entry_var.set('')
        elif re.match(pattern_faculty, input_text):
            # The input matches the faculty format, open faculty.py
            subprocess.Popen(['python', 'faculty.py'])
            self.entry_var.set('')
        else:
            # The input does not match any of the specified formats, show an error message
            messagebox.showerror("Invalid Format",
                                 "Please enter the correct OTP code format you received in your email.")


class ValidationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill="both")

        self.canvas.config(borderwidth=0, highlightthickness=0)

        # Load the background image using PIL
        self.bg_image = Image.open('Frame 14.png')
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
        image_path = 'banner.png'  # Replace with the path to your image
        if os.path.exists(image_path):
            image = Image.open(image_path)

            # Calculate the position of the image in the upper right corner
            image_width, image_height = image.size
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            image_x = screen_width // 8 - 180
            image_y = 80

            # Create a PhotoImage object from the cropped image
            image = ImageTk.PhotoImage(image)

            # Create a label to display the image with a transparent background
            image_label = tk.Label(self, image=image, bg="#D0CFD2")
            image_label.place(x=image_x, y=image_y)

            # Keep a reference to the image to prevent it from being garbage collected
            image_label.image = image
        else:
            print(f"Image file not found: {image_path}")

        # Add header text inside the rectangle
        header_text1 = self.canvas.create_text(screen_width // 2 + 5, 37,
                                                text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE",
                                                fill="black", font=("Cambria", 26))

        header_text = self.canvas.create_text(950, 350, text="WELCOME", fill="#862C3C",
                                              font=("Times New Roman", 160, 'bold'))
        header = self.canvas.create_text(948, 348, text="WELCOME", fill="white", font=("Times New Roman", 160, 'bold'))

        # Add subheader text below the header text
        subheader_text = self.canvas.create_text(screen_width // 2, 550, text="T U P C I A N S !", fill="white",
                                                 font=('Anonymous Pro', 70, 'bold', "italic"))
        sub_header = self.canvas.create_text(screen_width // 2 - 2, 548, text="T U P C I A N S !", fill="#862C3C",
                                             font=('Anonymous Pro', 70, 'bold', "italic"))

        # Create a button instead of clickable text
        scan_button = tk.Button(self, text="TAP TO SCAN YOUR ID", font=("Times New Roman", 35, 'italic'),
                                bg='#D9D9D9', fg='black', width=40, bd=0, command=self.on_scan_button_click)
        scan_button.place(x=screen_width // 2.7 - 250, y=screen_height - 370)


        # Load the button image
        button_image = Image.open("button.png")
        button_photo = ImageTk.PhotoImage(button_image)

        # Create a transparent button
        button = tk.Button(self, image=button_photo, bg='#570718', borderwidth=0, highlightthickness=0,
                           command=self.on_back_button_click)
        button.photo = button_photo  # Keep a reference to the image
        button.place(x=screen_width // 4 - 450, y=screen_height//2 + 350)  # Adjust the position as needed

        # Define scan_qr_code as a class method
    def scan_qr_code(self):
        def scanning_thread():
            cap = cv2.VideoCapture(0)

            while True:
                _, img = cap.read()

                # Process the frame to detect QR codes
                data = self.detect_qr_code(img)
                if data:
                    cap.release()
                    cv2.destroyAllWindows()

                    # Print the scanned data
                    print(f"Scanned QR Code Data: {data}")

                    # Extract the relevant portion matching the format "TUPC-XX-XXXX"
                    match = re.search(r'TUPC-\d{2}-\d{4}', data)
                    if match:
                        extracted_data = match.group()
                        self.validate_and_check(extracted_data)
                    else:
                        print("Invalid QR Code Format")

                    return

                cv2.imshow("Scan QR Code", img)

                if cv2.waitKey(1) == ord("q"):
                    break

            cap.release()

        # Create a new thread to perform the scanning
        scan_thread = threading.Thread(target=scanning_thread)
        scan_thread.start()

    def detect_qr_code(self, frame):
        # Create a QRCode detector
        detector = cv2.QRCodeDetector()

        # Detect and decode QR codes in the frame
        decoded_info, points, _ = detector.detectAndDecode(frame)

        if decoded_info:
            return decoded_info
        else:
            return None

    def validate_and_check(self, data):
        # Check if the scanned data matches the expected format "TUPC-XX-XXXX"
        if re.match(r'TUPC-\d{2}-\d{4}', data):
            # Check if the data exists in your MySQL database
            if self.check_database(data):
                message = f"Valid QR Code: ID Number {data} is now validated."
                messagebox.showinfo("QR Code Scanned", message)
                self.controller.show_frame('StartPage')
            else:
                message = "QR Code data exists in the correct format, but it was not found in the database."
                messagebox.showerror("QR Code Scanned", message)
        else:
            message = "Invalid QR Code Format. The format should be 'TUPC-XX-XXXX'."
            messagebox.showerror("QR Code Scanned", message)


    def check_database(self, data):
        try:
            # Connect to your MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Kiosk1234",
                port=3306,
                database="kiosk_db"
            )

            cursor = conn.cursor()

            # Replace this query with your actual database query
            query = "SELECT * FROM kiosk_db.enrollment_list WHERE `StudentNo.` = %s"
            cursor.execute(query, (data,))
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False

        except mysql.connector.Error as e:
            print("Database error:", e)
            return False

        finally:
            conn.close()


    # Function to execute when the button is clicked
    def on_back_button_click(self):
        self.controller.show_frame('MainMenu_Page')

    def on_get_started_button_click(self):
        # Switch to the main menu with three buttons
        self.controller.show_frame('StartPage')

    def on_scan_button_click(self):
        self.scan_qr_code()





if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()