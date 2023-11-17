import threading
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

from pyzbar import pyzbar


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
        for F in (StartPage, MainMenu_Page, RequestPage, MakerPage, ValidationPage, MatchingPage):
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
        self.bg_image = Image.open('up_bg.png')
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
            image_x = screen_width - 120
            image_y = 515

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
            image_x = screen_width // 2 - 650
            image_y =55

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
        header_text1 = self.canvas.create_text(screen_width // 2 - 22 + 25, 28,
                                                text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE",
                                                fill="black",
                                                font=("Cambria", 19))

        header_text = self.canvas.create_text(699, 250, text="WELCOME", fill="#862C3C",
                                         font=("Times New Roman", 111, 'bold'))
        header =self.canvas.create_text(699, 249, text="WELCOME", fill="white", font=("Times New Roman", 110, 'bold'))

        # Add subheader text below the header text
        subheader_text = self.canvas.create_text(screen_width // 2, 370, text="T U P C I A N S !", fill="white",
                                                     font=('Anonymous Pro', 50, 'bold', "italic"))
        sub_header = self.canvas.create_text(screen_width // 2 - 1, 369, text="T U P C I A N S !", fill="#862C3C", font=('Anonymous Pro', 50, 'bold', "italic"))

        # Add another text element below the subheader text
        note_text = self.canvas.create_text(screen_width // 1.7 - 400, 620,
                                            text=" Welcome to our ID Maker Kiosk, students, faculty, and alumni! We are thrilled to\n offer this convenient service to help you obtain your IDs. Whether you need a new\n or a replacement ID, we are here to assist you.",
                                            fill="white",
                                            font=("Times New Roman", 16, "italic"))

        # Add clickable text button
        clickable_text = self.canvas.create_text(screen_width // 1.3 + 45, 530, text="Proceed", fill="white",
                                                 font=("Times New Roman", 50, 'italic'))
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

        # Load the image you want to display
        image_path = 'logo_tup.jpg'  # Replace with your image file path
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image.thumbnail((85, 41))  # Adjust the size as needed
            image = ImageTk.PhotoImage(image)

            # Create a label to display the image
            image_label = tk.Label(self, image=image, bg="white", borderwidth=0, highlightthickness=0)
            image_label.photo = image
            image_label.place(x=345, y=8)  # Adjust the position as needed


        # Add header text inside the rectangle
        header_text1 = self.canvas.create_text(screen_width // 2 + 26, 28,
                                               text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE",
                                               fill="black", font=("Cambria", 18))

        header = self.canvas.create_text(screen_width // 2, 180, text="M A I N  M E N U", fill="black", font=("Cambria", 85, 'bold'))
        header2 = self.canvas.create_text(screen_width // 2 -4, 179, text="M A I N  M E N U", fill="white", font=("Cambria", 85, 'bold'))

        req_text = self.canvas.create_text(260, 565, text="REQUEST ID", fill="#5C1C1C", font=("Cambria", 30))

        maker_text = self.canvas.create_text(682, 565, text="GENERATE ID", fill="#5C1C1C", font=("Cambria", 30))

        validation_text = self.canvas.create_text(1102, 565, text="VALIDATE ID", fill="#5C1C1C", font=("Cambria", 30))

        # Create buttons with images
        req_button = tk.Button(self, image=self.image2, compound=tk.TOP, bg="black", width=199, height=180, bd=0, command=self.on_button1_click)
        self.canvas.create_window(162, 300, window=req_button, anchor="nw")

        maker_button = tk.Button(self, image=self.image3, compound=tk.TOP, bg="black", width=199, height=180, bd=0,  command=self.on_button2_click)
        self.canvas.create_window(582, 300, window=maker_button, anchor="nw")

        valid_button = tk.Button(self, image=self.image1, compound=tk.TOP, bg="black", width=199, height=180, bd=0, command=self.on_button3_click)
        self.canvas.create_window(1002, 300, window=valid_button, anchor="nw")

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
            image_label.place(x=110, y=6)  # Adjust the position as needed


        # Add header text below the header rectangle
        header_text_below = self.canvas.create_text(screen_width // 2, 90, text="REQUEST FORM", fill="white",
                                                    font=('cambria', 25, 'bold'))

        # Add header text below the header rectangle
        notetext_below = self.canvas.create_text(screen_width // 2 + 20, 130, text="Kindly provide the complete information needed in this online form.", fill="white",
                                                    font=('IBM Plex Mono', 14))

        # Add header text below the header rectangle
        note_text_below = self.canvas.create_text(screen_width // 2 + 20, 160, text="There is a 150 pesos ID fee to be paid at the Cashier's Office for the replacement.",
                                                 fill="white", font=('IBM Plex Mono', 14))

        # Create a label for the user's role in university
        role_label = self.canvas.create_text(screen_width // 1.5 - 719, 225, text="Role in University:",
                                             font=("Arial", 14), fill='white')

        self.role_var = tk.StringVar()
        role_combobox = ttk.Combobox(self, textvariable=self.role_var,
                                     values=["Student", "Employee", "Alumni"],
                                     font=("Arial", 12), state="readonly")
        role_combobox.place(x=370, y=210, width=750, height=25)
        role_combobox.set("Select your Role in University")  # Set the default value

        # Create a label for the user's email
        email_label = self.canvas.create_text(screen_width // 1.54 - 675, 265, text="GSFE/GMAIL Account:", font=("Arial", 14),
                                              fill='white')

        # Create an entry widget for the user's email
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(self, font=("Arial", 12))
        self.email_entry.place(x=370, y=250, width=750, height=25)

        # Create a label for the student ID
        id_number_label = self.canvas.create_text(screen_width // 1.55 - 714, 305, text="ID NUMBER:",
                                                  font=("Arial", 14),
                                                  fill='white')

        # Create an entry widget for the student ID
        self.id_number_var = tk.StringVar()
        self.id_number_entry = tk.Entry(self, font=("Arial", 12))
        self.id_number_entry.place(x=370, y=290, width=750, height=25)

        # Create a label for the student request
        request_type_label = self.canvas.create_text(screen_width // 1.49 - 718, 345, text="Type of ID Request:",
                                                     font=("Arial", 14), fill='white')

        self.type_var = tk.StringVar()
        request_type_combobox = ttk.Combobox(self, textvariable=self.type_var,
                                             values=[
                                                 "REPLACEMENT (For old students with lost ID)",
                                                 "REPLACEMENT (For old students with damaged ID that needs replacement)",
                                                 "New ID (For new students and alumni who don't have their ID's)"],
                                             font=("Arial", 12), state="readonly")
        request_type_combobox.place(x=370, y=330, width=750, height=25)
        request_type_combobox.set("Select Type of ID Request")

        # Create a label for the reason
        reason_label = self.canvas.create_text(screen_width // 1.51 - 719, 385, text="Specify Reason:", font=("Arial", 14),
                                               fill='white')

        self.reason_var = tk.StringVar()
        self.reason_entry = tk.Entry(self, font=("Arial", 12))
        self.reason_entry.place(x=370, y=370, width=750, height=25)

        # Create a label for the student lastname
        lastname_label = self.canvas.create_text(screen_width // 1.55 - 718, 425, text="Last Name:", font=("Arial", 14),
                                                 fill='white')

        # Create an entry widget for the student lastname
        self.lastname_var = tk.StringVar()
        self.lastname_entry = tk.Entry(self, font=("Arial", 12))
        self.lastname_entry.place(x=370, y=410, width=750, height=25)

        # Create a label for the student firstname
        firstname_label = self.canvas.create_text(screen_width // 1.55 - 718, 465, text="First Name:",
                                                  font=("Arial", 14),
                                                  fill='white')

        # Create an entry widget for the student firstname
        self.firstname_var = tk.StringVar()
        self.firstname_entry = tk.Entry(self, font=("Arial", 12))
        self.firstname_entry.place(x=370, y=450, width=750, height=25)

        # Create a label for the student middle name
        middlename_label = self.canvas.create_text(screen_width // 1.53 - 718, 505, text="Middle Name:",
                                                   font=("Arial", 14),
                                                   fill='white')

        # Create an entry widget for the student middle name
        self.middlename_var = tk.StringVar()
        self.middlename_entry = tk.Entry(self, font=("Arial", 12))
        self.middlename_entry.place(x=370, y=490, width=750, height=25)

        self.middlename_entry.bind("<Button-1>", self.show_system_keyboard)

        # Create a label for the student contact number
        contact_label = self.canvas.create_text(screen_width // 1.54 - 718, 545, text="Contact No.:",
                                                font=("Arial", 14),
                                                fill='white')

        # Create an entry widget for the student contact number
        self.contact_var = tk.StringVar()
        self.contact_entry = tk.Entry(self, font=("Arial", 12), textvariable=self.contact_var)
        self.contact_entry.place(x=370, y=530, width=750, height=25)
        self.contact_entry['validate'] = 'key'
        self.contact_entry['validatecommand'] = (self.contact_entry.register(self.on_validate_contact), '%P')

        # Create a label for the student program or course
        program_label = self.canvas.create_text(screen_width // 1.56 - 718, 585, text="Program:", font=("Arial", 14),
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
                                       font=('Arial', 12), state="readonly")
        course_combobox.place(x=370, y=570, width=750, height=25)
        course_combobox.set("Select your Program")

        # Create the "Clear" button
        clear_button = tk.Button(self, text="Clear", font=("IBM Plex Mono", 14, 'bold'), command=self.clear_form,
                                  width=12)
        clear_button.place(relx=0.06, rely=0.95, anchor="sw")

        # Create the "Submit" button
        self.submit_button = tk.Button(self, text="Submit", font=("IBM Plex Mono", 14, 'bold'), command=self.submit_form, width=12)
        self.submit_button.place(relx=0.83, rely=0.95, anchor="se")

        # Create the "Cancel" button
        cancel_button = tk.Button(self, text="Cancel", font=("IBM Plex Mono", 14, 'bold'), command=self.cancel_form, width=12)
        cancel_button.place(relx=0.96, rely=0.95, anchor="se")

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
        if all([(
                        self.role_var.get() != 'Select your Role in University' and self.email_entry.get() and self.id_number_entry.get() and self.type_var.get() != 'Select Type of ID Request' and
                        self.reason_entry.get() and self.lastname_entry.get() and self.firstname_entry.get() and self.middlename_entry.get() and self.contact_entry.get() and
                        self.course_var.get() != 'Select your Program')]):
            # Enable the "Submit" button if all fields are filled
            self.submit_button.config(state=tk.NORMAL)
        else:
            # Disable the "Submit" button if any field is empty
            self.submit_button.config(state=tk.DISABLED)

    def on_validate_contact(self, P):
        # P is the proposed text
        return P.isdigit() and len(P) <= 11

    def submit_form(self):
        selected_role = self.role_var.get()
        selected_request = self.type_var.get()
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
            confirmation_message = f"Role in University: {selected_role}\nEmail: {email}\nStudent ID Number: {id_number}\nType of ID Request: {selected_request}\nReason: {reason}\nLast Name: {lastname}\nFirst Name: {firstname}\nMiddle Name: {middlename}\nContact No.: {contact}\nProgram: {selected_course}\nIs the information correct?"

            # Show a message box to confirm the entered details
            user_confirmation = messagebox.askyesno("Confirmation of Request", confirmation_message)

            if user_confirmation:
                # Save the data to the database
                self.save_data_to_database(selected_role, email, id_number, selected_request, reason, lastname,
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
                self.contact_var.set('')
                self.course_var.set("Select your Program")

            else:
                return None

    def save_data_to_database(self, Role, Email, StudentID, Request, Reason, LastName, FirstName, MiddleName, ContactNo,
                              Program):
        # Establish a connection to the MySQL database
        db_request = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root030702",
            port=330,
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
        self.contact_var.set('')
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
        header_text1 = self.canvas.create_text(screen_width // 2 + 26, 28,
                                               text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE",
                                               fill="black", font=("Cambria", 18))

        # Load the image you want to display
        image_path = 'logo_tup.jpg'  # Replace with your image file path
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image.thumbnail((85, 41))  # Adjust the size as needed
            image = ImageTk.PhotoImage(image)

            # Create a label to display the image
            image_label = tk.Label(self, image=image, bg="white", borderwidth=0, highlightthickness=0)
            image_label.photo = image
            image_label.place(x=345, y=8)  # Adjust the position as needed

        # Add text below the subheader text
        text = self.canvas.create_text(screen_width // 1.61 - 150, 320, text="Enter the OTP sent to your email.",
                                           fill="black",
                                                 font=('Times New Roman', 50, 'bold'))
        subtext = self.canvas.create_text(screen_width // 1.61 - 150, 318,
                                       text="Enter the OTP sent to your email.",
                                       fill="white",
                                       font=('Times New Roman', 50, 'bold'))


        submit = tk.Button(self, text="SUBMIT", compound=tk.LEFT, bg="#CECFD3", width=18,
                           font=("Times New Roman", 25, 'italic'), command=self.validate_and_submit)
        self.canvas.create_window(650, 640, window=submit, anchor="s")

        backbutton_image = Image.open('back.png')
        self.backbutton_image = ImageTk.PhotoImage(backbutton_image)

        back_button = tk.Button(self, image=self.backbutton_image, compound=tk.LEFT, bg="#CECFD3", width=80, height=80,
                                bd=0,
                                command=self.on_back_button_click)
        self.canvas.create_window(20, 95, window=back_button, anchor="nw")

        # Add an entry widget
        self.entry_box_var = tk.StringVar()
        entry_box = tk.Entry(self, textvariable=self.entry_box_var, font=("cambria", 40, 'bold'), bg='#D9D9D9',
                             width=24, bd=0,
                             fg='black', justify="center")
        self.canvas.create_window(308, 485, window=entry_box, anchor="nw")

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
            self.entry_box_var.set('')
        elif re.match(pattern_student, input_text):
            # The input matches the student format, open student.py
            subprocess.Popen(['python', 'id_front.py'])
            self.entry_box_var.set('')
        elif re.match(pattern_faculty, input_text):
            # The input matches the faculty format, open faculty.py
            subprocess.Popen(['python', 'faculty.py'])
            self.entry_box_var.set('')
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
            image_x = screen_width // 2 - 650
            image_y = 55

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
        header_text1 = self.canvas.create_text(screen_width // 2 , 28,
                                                text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE",
                                                fill="black", font=("Cambria", 18))

        # Add header text below the header rectangle
        header_text_below = self.canvas.create_text(screen_width // 2, 230, text="WELCOME", fill="#862C3C",
                                                    font=("Times New Roman", 110, 'bold'))
        header_text_below2 = self.canvas.create_text(screen_width // 2, 228, text="WELCOME", fill="white",
                                                    font=("Times New Roman", 110, 'bold'))

        # Add subheader text below the header text
        subheader_text = self.canvas.create_text(screen_width // 2, 370, text="T U P C I A N S !", fill="white",
                                                 font=('Anonymous Pro', 50, 'bold', "italic"))
        sub_header = self.canvas.create_text(screen_width // 2 - 1, 369, text="T U P C I A N S !", fill="#862C3C",
                                             font=('Anonymous Pro', 50, 'bold', "italic"))

        # Create a button instead of clickable text
        scan_button = tk.Button(self, text="TAP TO SCAN YOUR ID", font=("Times New Roman", 28, 'italic'),
                                bg='#D9D9D9', fg='black', width=37, bd=0, command=self.on_scan_button_click)
        scan_button.place(x=screen_width // 3.3 - 105, y=screen_height // 2 + 98)

        # Load the button image
        button_image = Image.open("button.png")
        # Resize the button image to the desired size, e.g., (width, height)
        button_image = button_image.resize((90, 90))
        button_photo = ImageTk.PhotoImage(button_image)

        # Create a transparent button
        button = tk.Button(self, image=button_photo, bg='#570718', borderwidth=0, highlightthickness=0,
                           command=self.on_back_button_click)
        button.photo = button_photo  # Keep a reference to the image
        button.place(x=screen_width // 3.5 - 360, y=screen_height // 3.5 + 370)  # Adjust the position as needed

    # Function to execute when the button is clicked
    def on_back_button_click(self):
        self.on_get_started_button_click()

    def on_link_text_click(self, event):
        self.on_get_started_button_click()

    def on_get_started_button_click(self):
        # Switch to the main menu with three buttons
        self.controller.show_frame('MainMenu_Page')

    def on_scan_button_click(self):
        matching_page = self.controller.frames["MatchingPage"]
        matching_page.start_qr_scan_thread()


class MatchingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#5D1C1C')
        self.controller = controller
        self.photo = None
        self.camera_preview_initialized = False

        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.canvas.pack()

        # Create the camera preview label
        self.camera_preview_label = tk.Label(self)
        self.camera_preview_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)


        # Initialize variables to hold the camera capture and thread state
        self.cap = None
        self.thread_running = False

    def initialize_camera_on_enter(self):
        # Add your implementation here, for example:
        self.start_qr_scan_thread()

    def start_qr_scan_thread(self):
        # Create a new thread to run the QR code scanning process and camera preview
        qr_scan_thread = threading.Thread(target=self.start_qr_scan)
        qr_scan_thread.start()

    def start_qr_scan(self):
        # Start the camera and create the camera preview thread
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return
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


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()