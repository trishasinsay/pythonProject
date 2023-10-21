from tkinter import *
from PIL import Image, ImageTk

def on_resize(event):
    canvas.config(width=event.width, height=event.height)
    redraw_background()
    redraw_header()

def button_click(event):
    # Simulate underlining the text by modifying the tag's font option
    canvas.itemconfig("button", font=("Brush Script MT", 60, 'bold underline'))

    # Open another window and set its dimensions to match the screen
    new_window = Toplevel(window)
    new_window.title("New Window")

    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    new_window.geometry(f"{screen_width}x{screen_height}")

    # Make the new window resizable
    new_window.resizable(True, True)

    label = Label(new_window, text="This is another window")
    label.pack(fill=BOTH, expand=True)



def redraw_background():
    global background_image
    background_image = Image.open("bg.png")
    background_image = background_image.resize((canvas.winfo_width(), canvas.winfo_height()))
    background_image = ImageTk.PhotoImage(background_image)
    canvas.create_image(0, 0, anchor=NW, image=background_image)

def redraw_header():
    canvas.create_rectangle(0, 0, canvas.winfo_width(), 50, fill='#D8D8D8')  # Adjust the color and size as needed

    image_inside_rectangle = Image.open("header_logo.png")  # Replace with your image path
    image_inside_rectangle = image_inside_rectangle.resize((41, 41))  # Adjust the size as needed
    image_inside_rectangle = ImageTk.PhotoImage(image_inside_rectangle)
    canvas.create_image(10, 10, anchor=NW, image=image_inside_rectangle)

    # Add text to the header and align to center
    header_text = "TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES - CAVITE"
    text_x = canvas.winfo_width() / 2  # Calculate x-coordinate for center alignment

    canvas.create_text(text_x, 25, text=header_text, fill="black", font=("Cambria", 20, 'bold'), tags="header")

    # Add header text below the rectangle
    header_text_below = "WELCOME"
    canvas.create_text(670, 230, text=header_text_below, fill="white", font=("League Spartan", 100, 'bold'))

    # Add sub-header text below the header
    header_text_below = "TUPCIANS!"
    canvas.create_text(850, 330, text=header_text_below, fill="#CF0F13", font=("Bangers", 70, 'bold'))

    # Create a text element that acts like a button
    button_text = "Get Started >>"
    canvas.create_text(1050, 580, text=button_text, fill="white", font=("Brush Script MT", 60, 'bold'), tags="button")
    canvas.tag_bind("button", "<Button-1>", button_click)

window = Tk()

# Set the background color of the window to dark gray
window.configure(bg='black')

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size to fit the screen with a 1-pixel border
window.geometry(f"{screen_width}x{screen_height}")

window.title("TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES - CAVITE")
icon = PhotoImage(file='tup logo 1.png')
window.iconphoto(True, icon)

# Create a Canvas widget that covers the entire window
canvas = Canvas(window, width=screen_width, height=screen_height, bg='dark gray')
canvas.pack()

# Bind Canvas to the Configure event of the window
window.bind("<Configure>", on_resize)

# Load and display the background image and header
redraw_background()
redraw_header()

window.mainloop()


def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # Load the background image using PIL
    background_image = Image.open('bg.png')  # Replace with your background image path

    # Create a Canvas to display the background image
    self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
    self.canvas.pack()

    # Update the background image
        self.update_background(background_image)
# Create a label for the Main Menu
        mainmenu_label = tk.Label(self.canvas, text="MAIN MENU", font=('caveat brush', 55), bg='#D8D8D8', fg='#5D1C1C')
        mainmenu_label.grid(row=0, column=1, pady=40, padx=20, sticky='N')

        # Create the buttons with background color and image on top
        button1 = tk.Button(self.canvas, compound=tk.TOP, text='ID Request', height=370, width=300,
                            command=self.on_button1_click, bd=0)
        button1.grid(row=0, column=0, pady=200, padx=90, sticky='w')

        button2 = tk.Button(self.canvas, compound=tk.TOP, text='ID Maker', bg='#5D1C1C', height=370, width=330,
                            command=self.on_button2_click, bd=0)
        button2.grid(row=0, column=1, pady=200, padx=20, sticky='w')

        button3 = tk.Button(self.canvas, compound=tk.TOP, text='ID Validation', height=370, width=300,
                            command=self.on_button3_click, bd=0)
        button3.grid(row=0, column=2, pady=200, padx=70, sticky='e')

    def on_button1_click(self):
        # Switch to the ID Request page
        request_page_frame = RequestPage(self.controller, self.controller)
        request_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('RequestPage')

    def on_button2_click(self):
        # Switch to the ID Maker page
        maker_page_frame = MakerPage(self.controller, self.controller)
        maker_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('MakerPage')

    def on_button3_click(self):
        # Switch to the ID Validation page
        validation_page_frame = ValidationPage(self.controller, self.controller)
        validation_page_frame.pack(fill='both', expand=True)
        self.controller.show_frame('ValidationPage')

    def update_background(self, image):
        # Get the screen width and height
        screen_width = self.winfo_width()
        screen_height = self.winfo_height()

        # Resize the background image to fit the window
        resized_bg_image = image.resize((screen_width, screen_height))

        # Create a PhotoImage object from the resized image
        self.background_image = ImageTk.PhotoImage(resized_bg_image)

        # Update the canvas image
        self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)

        ---------------------


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


-------------------

# Create a header using a Canvas widget
        header_canvas = tk.Canvas(self, bg="black", height=50)  # Adjust the height and color as needed
        header_canvas.pack(fill=tk.X)

        # Remove the border and highlight
        header_canvas.config(borderwidth=0, highlightthickness=0)

        # Create text on the header
        header_canvas.create_text(365, 10, anchor=tk.NW, text="TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE", font=("Cambria", 18, "bold"),
                                  fill="white")

        # Create an Image widget for the upper left image
        image_path = 'tup.jpg'  # Replace with your image file path
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image.thumbnail((90, 40))  # Adjust the size as needed
            image = ImageTk.PhotoImage(image)

            image_label = tk.Label(self, image=image, bg="white")
            image_label.photo = image
            image_label.place(x=310, y=4)  # Adjust the position as needed

            # Remove the border and highlight for the image
            image_label.config(borderwidth=0, highlightthickness=0)

