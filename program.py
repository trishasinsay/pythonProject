import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
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
        self.canvas.coords(sub_heading_label, self.winfo_screenwidth() // 2 + 210,
                           self.winfo_screenheight() // 3 + 160)

        # Create the "Get Started" button
        get_started_button = tk.Button(self, text='Get Started', font=('inter', 20, 'bold'),
                                       command=self.on_get_started_button_click, bg='#5D1C1C', fg='white',
                                       width=16, height=2)

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
        button1 = tk.Button(self, image=image1, compound=tk.TOP, bg='#5D1C1C', height=300, width=330,
                            command=self.on_button1_click, bd=0)
        button2 = tk.Button(self, image=image2, compound=tk.TOP, bg='#5D1C1C', height=300, width=330,
                            command=self.on_button2_click, bd=0)
        button3 = tk.Button(self, image=image3, compound=tk.TOP, bg='#5D1C1C', height=300, width=330,
                            command=self.on_button3_click, bd=0)

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
        # Handle button 2 click event
        pass

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

        # Create Scan button
        start_scan_button = tk.Button(self, text='PLEASE SCAN YOUR ID', font=('inter', 20, 'bold'),
                                      command=self.on_start_scan_button_click, bg='#5D1C1C', fg='white',
                                      width=20, height=2)

        # Place the button below the sub-heading label
        self.canvas.create_window(self.winfo_screenwidth() // 2 + 250, self.winfo_screenheight() // 2 + 215,
                                  window=start_scan_button)

    def on_start_scan_button_click(self):
        start_scan_button = tk.Button(self, text="Start Scan", command=self.start_qr_scan)
        start_scan_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        self.video_widget = VideoWidget()
        self.video_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.video_widget.start_camera()

    def start_qr_scan(self):
        qr_code_data = self.decode_qr_code()
        if qr_code_data:
            self.scan_label.config

    def on_qr_code_scanned(self, qr_code_data):
        self.video_widget.stop_camera()
        self.scan_label.config(text=f'Success! QR Code: {qr_code_data}')
        messagebox.showinfo('QR Code Scanned', f'Success! QR Code: {qr_code_data}')


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