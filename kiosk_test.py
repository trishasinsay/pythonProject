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
        header_text_below = self.canvas.create_text(screen_width // 2, 220, text="WELCOME", fill="white",
                                                    font=("Cambria", 110, 'bold'))

        # Add subheader text below the header text
        subheader_text = self.canvas.create_text(screen_width // 1.55, 335, text="TUPCIANS!", fill="#CF0F13",
                                                     font=('bangers', 70, 'bold'))

        # Add another text element below the subheader text
        note_text = self.canvas.create_text(screen_width // 1.45, 450,
                                            text=" Welcome, students, faculties, and alumni, to our ID Maker Kiosk! We are thrilled to\n offer this convenient service to help you obtain your IDs. Whether you're new or need\n a replacement ID, we're here to assist you.",
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
                                     values=["Student", "Faculty", "Alumni"],
                                     font=("Arial", 12), state="readonly")
        role_combobox.place(x=370, y=210, width=300, height=25)
        role_combobox.set("Select your Role in University")  # Set the default value

        # Create a label for the user's email
        email_label = self.canvas.create_text(screen_width // 1.54 - 719, 265, text="GSFE Email:", font=("Arial", 14),
                                              fill='white')

        # Create an entry widget for the user's email
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(self, font=("Arial", 12))
        self.email_entry.place(x=370, y=250, width=600, height=25)

        # Create a label for the student ID
        id_number_label = self.canvas.create_text(screen_width // 1.55 - 719, 305, text="Student ID:",
                                                  font=("Arial", 14),
                                                  fill='white')

        # Create an entry widget for the student ID
        self.id_number_var = tk.StringVar()
        self.id_number_entry = tk.Entry(self, font=("Arial", 12))
        self.id_number_entry.place(x=370, y=290, width=300, height=25)

        # Create a label for the student request
        request_type_label = self.canvas.create_text(screen_width // 1.49 - 718, 345, text="Type of ID Request:",
                                                     font=("Arial", 14), fill='white')

        self.type_var = tk.StringVar()
        request_type_combobox = ttk.Combobox(self, textvariable=self.type_var,
                                             values=[
                                                 "REPLACEMENT(For old students with lost ID",
                                                 "REPLACEMENT(For old students with damaged ID that needs replacement",
                                                 "New ID"],
                                             font=("Arial", 12), state="readonly")
        request_type_combobox.place(x=370, y=330, width=600, height=25)
        request_type_combobox.set("Select Type of ID Request")

        # Create a label for the reason
        reason_label = self.canvas.create_text(screen_width // 1.57 - 719, 385, text="Reason:", font=("Arial", 14),
                                               fill='white')

        self.reason_var = tk.StringVar()
        self.reason_entry = tk.Entry(self, font=("Arial", 12))
        self.reason_entry.place(x=370, y=370, width=700, height=25)

        # Create a label for the student lastname
        lastname_label = self.canvas.create_text(screen_width // 1.55 - 718, 425, text="Last Name:", font=("Arial", 14),
                                                 fill='white')

        # Create an entry widget for the student lastname
        self.lastname_var = tk.StringVar()
        self.lastname_entry = tk.Entry(self, font=("Arial", 12))
        self.lastname_entry.place(x=370, y=410, width=550, height=25)

        # Create a label for the student firstname
        firstname_label = self.canvas.create_text(screen_width // 1.55 - 718, 465, text="First Name:",
                                                  font=("Arial", 14),
                                                  fill='white')

        # Create an entry widget for the student firstname
        self.firstname_var = tk.StringVar()
        self.firstname_entry = tk.Entry(self, font=("Arial", 12))
        self.firstname_entry.place(x=370, y=450, width=550, height=25)

        # Create a label for the student middle name
        middlename_label = self.canvas.create_text(screen_width // 1.53 - 718, 505, text="Middle Name:",
                                                   font=("Arial", 14),
                                                   fill='white')

        # Create an entry widget for the student middle name
        self.middlename_var = tk.StringVar()
        self.middlename_entry = tk.Entry(self, font=("Arial", 12))
        self.middlename_entry.place(x=370, y=490, width=550, height=25)

        # Create a label for the student contact number
        contact_label = self.canvas.create_text(screen_width // 1.54 - 718, 545, text="Contact No.:",
                                                font=("Arial", 14),
                                                fill='white')

        # Create an entry widget for the student contact number
        self.contact_var = tk.StringVar()
        self.contact_entry = tk.Entry(self, font=("Arial", 12))
        self.contact_entry.place(x=370, y=530, width=300, height=25)

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
        course_combobox.place(x=370, y=570, width=550, height=25)
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
        header_text_below = self.canvas.create_text(screen_width // 2 - 175, 140, text="TUPC", fill="#CF0F13",
                                                    font=("Bangers", 80, 'bold'))

        # Add header text below the header rectangle
        header1_text_below = self.canvas.create_text(screen_width // 2 + 170, 140, text="KIOSK", fill="white",
                                                    font=("Bangers", 78, 'bold'))

        # Add subheader text below the header text
        subheader_text = self.canvas.create_text(screen_width // 1.96, 250, text="ID MAKER", fill="white",
                                                 font=('bangers', 80, 'bold'))

        # Add text below the subheader text
        text = self.canvas.create_text(screen_width // 1.65, 390, text="Enter your OTP code here", fill="white",
                                                 font=('caveat brush', 35))

        # Add an entry widget
        self.entry_var = tk.StringVar()
        entry_widget = tk.Entry(self, textvariable=self.entry_var, font=("cambria", 35, 'bold'), bg='#6C6C6C', fg='white', justify="center")
        entry_widget.place(x=screen_width // 2.8, y=screen_height // 2 + 50, width=700, height=80)

        # Create a button instead of clickable text
        submit_button = tk.Button(self, text="Submit", font=("Bitter", 20, 'bold', 'italic'),
                                bg='#641010', fg='white', width=20, height= 2, command=self.validate_and_submit)
        submit_button.place(x=screen_width // 2.35 + 82 ,y=screen_height // 2 + 155)

        # Add clickable text button
        link = self.canvas.create_text(screen_width // 6 - 100, 50, text="Tupcuitc.com", fill="white",
                                       font=("Bitter", 20, 'bold', 'italic'))

        self.canvas.tag_bind(link, "<Button-1>", self.on_link_text_click)

        # Load the button image
        button_image = Image.open("back.png")
        button_photo = ImageTk.PhotoImage(button_image)

        # Create a transparent button
        button = tk.Button(self, image=button_photo, bg='#141516', borderwidth=0, highlightthickness=0,
                           command=self.on_back_button_click)
        button.photo = button_photo  # Keep a reference to the image
        button.place(x=screen_width // 2.2 + 650, y=screen_height // 2 + 220)  # Adjust the position as needed

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
        input_text = self.entry_var.get()

        # Define a regular expression pattern to match the format "A-XXXXXX"
        pattern = r'^[A]-\d{6}$'

        if re.match(pattern, input_text):
            # The input matches the format, you can proceed
            subprocess.Popen(['python', 'id_front.py'])
            self.entry_var.set('')
        else:
            # The input does not match the format, show a messagebox
            messagebox.showerror("Invalid Format", "Please enter the right OTP code format you recieved in your email.")


class ValidationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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

        # Create a button instead of clickable text
        scan_button = tk.Button(self, text="TAP TO SCAN YOUR COR", font=("cambria", 28, 'bold'),
                                bg='#661112', fg='white', width=27, height=1, command=self.on_scan_button_click)
        scan_button.place(x=screen_width // 2.35 - 100, y=screen_height // 2 + 120)

        # Add clickable text button
        link = self.canvas.create_text(screen_width // 6 - 100, 50, text="Tupcuitc.com", fill="white",
                                       font=("Bitter", 20, 'bold', 'italic'))

        self.canvas.tag_bind(link, "<Button-1>", self.on_link_text_click)

        # Load the button image
        button_image = Image.open("back.png")
        button_photo = ImageTk.PhotoImage(button_image)

        # Create a transparent button
        button = tk.Button(self, image=button_photo, bg='#141516', borderwidth=0, highlightthickness=0,
                           command=self.on_back_button_click)
        button.photo = button_photo  # Keep a reference to the image
        button.place(x=screen_width // 2.2 + 650, y=screen_height // 2 + 220)  # Adjust the position as needed


        # Add another text element below the subheader text
        note_text = self.canvas.create_text(screen_width // 1.38 - 200, 600,
                                            text="*Note: Please place your COR to the designated place before scanning start.",
                                            fill="white", font=("roboto", 14))

    # Function to execute when the button is clicked
    def on_back_button_click(self):
        self.on_get_started_button_click()

    def on_link_text_click(self, event):
        self.on_get_started_button_click()

    def on_get_started_button_click(self):
        # Switch to the main menu with three buttons
        self.controller.show_frame('MainMenu_Page')

    def on_scan_button_click(self):
        # Switch to the main menu with three buttons
        self.controller.frames["MatchingPage"].initialize_camera_on_enter()
        self.controller.show_frame("MatchingPage")


class MatchingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#5D1C1C')
        self.controller = controller
        self.photo = None
        self.camera_preview_initialized = False

        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.canvas.pack()

        # Create a variable to keep track of whether a match has been found
        self.match_found = False

        # Create a variable to control whether scanning should continue
        self.continue_scanning = True

        # Create a canvas to display the camera preview
        self.camera_preview_label = tk.Label(self, width=900, height=650, bg='#5D1C1C')
        self.camera_preview_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        # Create a label for the text extraction results
        self.text_result_label = tk.Label(self, text='', font=('inter', 14), fg='white', bg='#5D1C1C')
        self.text_result_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Create a StringVar to hold the extracted text
        self.extracted_text_var = tk.StringVar()


    def initialize_camera_on_enter(self):
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

    def start_validation(self):
        self.initialize_camera_on_enter()
        self.match_found = False
        self.continue_scanning = True

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
            x1, y1, x2, y2 = int(x1 * scale_factor), int(y1 * scale_factor), int(x2 * scale_factor), int(
                y2 * scale_factor)
            image_rgb = cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 0, 255), 2)

        return extracted_text, image_rgb

    def stop_camera(self):
        # Release the camera
        if self.cap is not None:
            self.cap.release()
        self.camera_preview_initialized = False  # Reset the camera initialization flag

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
                port=330,  # Use an integer for the port
                database="kiosk_db"
            )

            cursor = db.cursor()

            # The SQL query should be written with backticks for field names with spaces and specify the table name.
            cursor.execute("SELECT `StudentNo.` FROM enrollment_list")

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
                        self.initialize_camera_on_enter()

                        # Clear previous text and image
                        self.text_result_label.config(text='')
                        self.camera_preview_label.config(image='')

                    else:
                        print("Not Matched")
                        # Show a message box with scan again or cancel options
                        response = messagebox.askquestion("Validation Failed",
                                                          "The ID is not in the database. Scan again?",
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
                response = messagebox.askquestion("Validation Failed", "No valid ID format found. Scan again?",
                                                  icon='warning')
                if response == 'yes':
                    # User chose to scan again, do nothing as the camera will continue scanning
                    pass
                else:
                    # User chose to cancel, go back to the StartPage
                    self.controller.show_frame("StartPage")
        else:
            print("No text detected")

    def go_to_matching_page(self):
        self.start_validation()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()