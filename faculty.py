from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image as I
from PIL import ImageTk as IT
from PIL import ImageDraw as ID
from PIL import ImageFont as IF
from PIL import Image, ImageOps, ImageChops, ImageFilter
import qrcode as Q
from resizeimage import resizeimage as re
import random
import datetime
import cv2
import textwrap
import numpy as np
import os
import re as RE
import subprocess

# WIN SETTINGS
title = 'TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES - CAVITE CAMPUS KIOSK ID MAKER'
size = '1366x768'
icon = ''
res = 0
W = [title, size, res, icon]

# FONTS
F1 = ('cambria', 20)
F2 = ('cambria', 16, 'bold')
F3 = ('cambria', 14, 'bold')
F4 = ('cambria italic', 10)
F5 = ('cambria', 12, 'bold')

class Win:
    def __init__(self, root):
        self.root = root
        self.root.title(W[0])
        self.root.geometry(W[1])

        # Set window icon
        self.root.iconbitmap('C:/Users/Trisha/PycharmProjects/pythonProject/tup-logo-1.ico')

        # Load the background image
        bg_image = Image.open('maroon.png')
        bg_image = bg_image.resize((1366, 768))  # Adjust the size to match your window size

        self.bg_image = IT.PhotoImage(bg_image)

        # Create a Label to display the background image
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # MAIN LABEL
        self.main_lab = Label(self.root, text=title, font=F1, pady=10, bg='black', fg='#ffffff')
        self.main_lab.pack(fill='x')  # Expand horizontally with the window

        # LOGO
        self.width = 50
        self.height = 49
        self.Logo_F = Frame(self.main_lab, relief=SUNKEN)
        self.Logo_F.pack(side='left', padx=30, pady=2)  # Adjust placement as needed

        self.img = I.open('tup.jpg')
        self.res_img = self.img.resize((self.width, self.height))
        self.Tk_Image = IT.PhotoImage(self.res_img)

        self.Logo_L = Label(self.Logo_F, image=self.Tk_Image, bg='black')
        self.Logo_L.pack(fill='both', expand=True)  # Expand both horizontally and vertically

        # FRAMES
        self.F1 = Frame(self.root, relief=SUNKEN, bd=1, bg='#B29999', width=500, height=500)  # Adjust width and height
        self.F1.pack(side='left', padx=20, pady=20, fill='both', expand=True)  # Expand both horizontally and vertically

        self.F2 = Frame(self.root, relief=SUNKEN, bd=1, bg='#B29999', width=500, height=400)  # Adjust width and height
        self.F2.pack(side='right', padx=20, pady=20, fill='both', expand=True)  # Expand both horizontally and vertically

        self.F1_title = Label(self.F1, bg='black', fg='#FFFFFF', text='Personal Details', font=F1)
        self.F1_title.place(x=0, y=0, relwidth=1)

        self.F2_title = Label(self.F2, bg='black', fg='#FFFFFF', text='ID Preview', font=F1)
        self.F2_title.place(x=0, y=0, relwidth=1)

        # LABELS
        self.L1 = Label(self.F1, text='ID NUMBER', font=F3, bg='#B29999').place(x=10, y=60)
        self.L2 = Label(self.F1, text='FULL NAME', font=F3, bg='#B29999').place(x=10, y=100)
        self.L3 = Label(self.F1, text='POSITION', font=F3, bg='#B29999').place(x=10, y=140)
        self.L4 = Label(self.F1, text='DEPARTMENT', font=F3, bg='#B29999').place(x=10, y=180)
        self.L5 = Label(self.F1, text='SIGNATURE', font=F3, bg='#B29999').place(x=10, y=290)
        self.L6 = Label(self.F1, text='*Note: Please answer all fields honestly and check your information before\npressing "Next" button and Use CAPITAL LETTERS only', font=F4, bg='#B29999')
        self.L6.place(x=120, y=220)
        self.L7 = Label(self.F1,text='*Note: When you are capturing image, press the ENTER KEY to capture your image',font=F4, bg='#B29999')
        self.L7.place(x=90, y=255)

        self.ID = StringVar()
        self.Fname = StringVar()
        self.position = StringVar()
        self.department = StringVar()

        # Add a placeholder text to Entry widget E1
        self.E1 = Entry(self.F1, font=F3, textvariable=self.ID)
        self.E1.place(x=210, y=60, width=400)
        self.E1.insert(0, "XX-XXX")  # Placeholder text
        self.E1.config(fg="gray")  # Set text color to gray
        self.E1.bind("<FocusIn>", self.on_entry_click_id)
        self.E1.bind("<FocusOut>", self.on_focus_out_id)


        self.E2 = Entry(self.F1, font=F3, textvariable=self.Fname).place(x=208, y=100, width=400)
        self.E3 = ttk.Combobox(self.F1, font=F3, state='readonly', textvariable=self.position)
        self.E3['values'] = ("Select your position",
                             "Faculty", "Admin", "Instructor I", "Instructor II", 'Instructor III', 'Asst. Prof I', "Asst. Prof II", "Asst. Prof III", "Asst. Prof IV",
                             "Assoc. Prof I", "Assoc. Prof II", "Assoc. Prof III", "Assoc. Prof IV", "Assoc. Prof V", "Professor I",
                             "Professor II", "Professor III", "Professor IV", "Professor V", "Professor VI")
        self.E3.current(0)
        self.E3.place(x=208, y=140, width=400)
        self.E4 = ttk.Combobox(self.F1, font=F3, state='readonly', textvariable=self.department)
        self.E4['values'] = ("Select your Department",
                             "INDUSTRIAL TECHNOLOGY DEPT.", "MATH AND SCIENCE DEPT.", 'LIBERAL ARTS DEPT.', 'ENGINEERING SCIENCES DEPT.',
                             "PHYSICAL EDUCATION DEPT.", "INDUSTRIAL EDUCATION DEPT.", "ADMINISTRATIVE SERVICES", "FINANCE SERVICES", "AUXILIARY SERVICES")
        self.E4.current(0)
        self.E4.place(x=208, y=180, width=400)


        # BUTTON
        self.B1 = Button(self.F1, text='Generate', font=F2, command=self.generate)
        self.B1.place(x=20, y=490, width=180)

        self.B2 = Button(self.F1, text='Clear', font=F2, command=self.clear)
        self.B2.place(x=430, y=490, width=180)

        self.B3 = Button(self.F1, text='Capture', font=F2, command=self.photo_capture)
        self.B3.place(x=220, y=490, width=180)

        self.B4 = Button(self.root, text='Next', font=F2, command=self.next, bg='#5D1C1C', fg='white', state='disabled')
        self.B4.place(x=1130, y=620, width=200)

        # MESSAGE BOX
        self.message = ''
        self.message_F = Frame(self.F1, relief=SUNKEN, bd=1)
        self.message_F.place(x=15, y=550, width=600, height=30)

        self.message_L = Label(self.message_F, text=self.message, font=F3, bd=1)
        self.message_L.place(x=0, y=0, relwidth=1, relheight=1)

        # SIGNATURE
        self.is_drawing = False
        self.last_x = 0
        self.last_y = 0

        self.signature_canvas = Canvas(self.F1, relief=SUNKEN, bg='white')
        self.signature_canvas.place(x=20, y=330, width=585, height=130)

        # Bind mouse events to the canvas
        self.signature_canvas.bind("<Button-1>", self.start_drawing)
        self.signature_canvas.bind("<B1-Motion>", self.draw)
        self.signature_canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.signature_drawn = False

        # F2
        self.ID_Frame = Frame(self.F2, relief=SUNKEN)
        self.ID_Frame.place(x=200, y=100, width=255, height=380)

        self.ID_L = Label(self.ID_Frame, text='ID\nCard\nNot Found', font=F1, bg='#B29999')
        self.ID_L.place(x=0, y=0, relwidth=1, relheight=1)

    def start_drawing(self, event):
        self.is_drawing = True
        self.last_x = event.x
        self.last_y = event.y
        self.signature_coords = []  # Start with an empty list for new signature

    def draw(self, event):
        if self.is_drawing:
            line_width = 2  # Adjust this value for the desired line thickness
            line_color = 'black'  # You can change the color to your preference
            self.signature_coords.append((event.x, event.y))
            if len(self.signature_coords) > 1:
                x0, y0 = self.signature_coords[-2]
                x1, y1 = self.signature_coords[-1]
                self.signature_canvas.create_line(x0, y0, x1, y1, fill=line_color, width=line_width, smooth=True)

    def stop_drawing(self, event):
        self.is_drawing = False
        self.signature_drawn = True

    def on_entry_click_id(self, event):
        if self.E1.get() == "XX-XXX":
            self.E1.delete(0, "end")
            self.E1.config(fg="black")

    def on_focus_out_id(self, event):
        if self.E1.get() == "":
            self.E1.insert(0, "XX-XXX")
            self.E1.config(fg="gray")

    def on_entry_ID(self, event):
        current_text = self.E1.get()
        if current_text == "XX-XXX ":
            self.E1.delete(0, "end")
            self.E1.config(fg="black")

    def on_focus_out_ID(self, event):
        if self.E1.get() == "":
            self.E1.insert(0, "XX-XXX")
            self.E1.config(fg="gray")

    def photo_capture(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, photo = cap.read()

            # Get the screen dimensions
            screen_width, screen_height = 1366, 768  # Replace with your screen dimensions

            # Calculate the position for the window to be centered
            window_x = (screen_width - photo.shape[1]) // 2
            window_y = (screen_height - photo.shape[0]) // 2

            # Create a window and move it to the center
            cv2.namedWindow('Take a Picture')
            cv2.moveWindow('Take a Picture', window_x, window_y)
            cv2.imshow('Take a Picture', photo)

            if cv2.waitKey(1) == 13:  # Press Enter key to capture the image
                self.captured_photo = photo.copy()
                break

        cv2.destroyAllWindows()

        if self.captured_photo is not None:
            # Save the captured photo with a unique ID (e.g., timestamp)
            current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            photo_filename = f'captured_photos/photo_{current_time}.jpg'
            cv2.imwrite(photo_filename, self.captured_photo)

            # Process the captured photo and save it as needed (resize, paste on ID card, etc.)
            # Example: Resize the photo to fit the ID card
            resized_photo = cv2.resize(self.captured_photo, (200, 200))

            # Save the processed photo
            processed_photo_filename = f'processed_photos/photo_{current_time}.jpg'
            cv2.imwrite(processed_photo_filename, resized_photo)

    def generate(self):
        # Check if ID follows the specified format
        if not RE.match(r'^\w{2}-\w{3}$', self.ID.get()):
            self.message = 'ID format should be XX-XXX'
            self.message_L.config(text=self.message, fg='red')
            self.B4.config(state='disabled')
            return

        if self.ID.get() == '' or self.Fname.get() == '' or self.position.get() == '' or self.department.get() == '' :
            self.message = 'Please answer all input fields'
            self.message_L.config(text=self.message, fg='red')
            self.B4.config(state='disabled')

        elif self.E3.current() == 0:
            self.message = 'Please select your position'
            self.message_L.config(text=self.message, fg='red')
            self.B4.config(state='disabled')

        elif self.E4.current() == 0:
            self.message = 'Please select your department'
            self.message_L.config(text=self.message, fg='red')
            self.B4.config(state='disabled')

        elif not hasattr(self, 'captured_photo'):
            self.message = 'Please capture your photo'
            self.message_L.config(text=self.message, fg='red')
            self.B4.config(state='disabled')

        elif not self.signature_drawn:
            self.message = 'Please provide a signature'
            self.message_L.config(text=self.message, fg='red')
            self.B4.config(state='disabled')

        else:
            font = IF.truetype(font='Arial Bold.ttf', size=9)
            font1 = IF.truetype(font='Arial Bold.ttf', size=8)
            font2 = IF.truetype(font='Arial Bold.ttf', size=10)
            font3 = IF.truetype(font='Arial Bold.ttf', size=10)
            font4 = IF.truetype(font='arial.ttf', size=6)

            background_image = I.open('faculty_temp.png')
            background_image = background_image.resize((205, 327))

            self.image_c = background_image.copy()
            self.Draw = ID.Draw(self.image_c)

            angle = 270
            self.Draw.text((76.8, 303), self.ID.get(), fill='black', font=font3)
            self.Draw.text((120, 213), self.Fname.get(), fill='black', font=font, anchor='mm')
            self.Draw.text((120, 227), self.position.get(), fill='black', font=font1, anchor='mm')

            # Rotate the department text before pasting it onto the ID card
            department_text = self.department.get()
            department_font = IF.truetype(font='Arial Bold.ttf', size=12)
            department_text_image = I.new('RGBA', (225, 29), '#bd2031')  # Create a transparent image
            department_draw = ID.Draw(department_text_image)
            department_draw.text((107, 15), department_text, fill='white', font=department_font, anchor='mm')

            # Rotate the text by the desired angle (e.g., 45 degrees)
            rotated_department_text_image = department_text_image.rotate(90, expand=True)

            # Paste the rotated department text onto the ID card image
            self.image_c.paste(rotated_department_text_image,
                               (8, 78))  # Adjust x and y positions as needed
            # Create a new blank signature image
            signature_image = Image.new('RGBA', (585, 150))

            # Draw the captured signature onto the new image
            draw = ID.Draw(signature_image)
            line_color = (0, 0, 0, 255)  # Black color with full opacity
            line_width = 3  # Adjust this value for the desired line thickness

            for i in range(1, len(self.signature_coords)):
                x0, y0 = self.signature_coords[i - 1]
                x1, y1 = self.signature_coords[i]
                draw.line([x0, y0, x1, y1], fill=line_color, width=line_width)

            # Save the signature image as a PNG
            signature_filename = f'signatures/signature_{self.ID.get()}.png'
            signature_image.save(signature_filename, 'PNG')

            # Load the saved signature image and remove the background
            if os.path.exists(signature_filename):
                signature_image = Image.open(signature_filename)

                # Remove the background (make it transparent)
                signature_image = signature_image.convert("RGBA")
                data = signature_image.getdata()

                new_data = []
                for item in data:
                    if item[:3] == (255, 255, 255):
                        new_data.append((255, 255, 255, 0))  # Replace white background with transparency
                    else:
                        new_data.append(item)

                signature_image.putdata(new_data)

                # Resize the signature image to the desired size
                new_signature_size = (80, 41)  # Adjust the size as needed
                signature_image = signature_image.resize(new_signature_size)

                # Paste the signature image onto the ID card
                self.image_c.paste(signature_image, (43, 262))  # Adjust the position as needed

            self.Qrcode = Q.QRCode(version=1, box_size=10, border=1)
            self.Qrcode.add_data(f'{self.Fname.get()} | {self.ID.get()}')
            self.Qrcode.make(fit=True)
            self.Qr = self.Qrcode.make_image(fill_color='#000000', back_color='#ffffff')
            self.Qr.save('Faculty QR\ID NO._ ' + str(self.ID.get()) + '.png')
            self.Qr_res = re.resize_cover(self.Qr, [67.2, 67.2])
            self.image_c.paste(self.Qr_res, (129, 252))

            # Load the captured image
            if hasattr(self, 'captured_photo'):
                # Process the captured photo and paste it onto the ID card
                resized_photo = cv2.resize(self.captured_photo, (90, 96))  # Adjust the size as needed
                photo_paste = I.fromarray(cv2.cvtColor(resized_photo, cv2.COLOR_BGR2RGB))
                self.image_c.paste(photo_paste, (74, 101))  # Adjust the position as needed

            # Save the generated ID card as a PNG image
            id_card_filename = 'Faculty ID\ID NO._' + str(self.ID.get()) + '.png'
            self.image_c.save(id_card_filename, "PNG")
            self.res_c = self.image_c.resize((255, 380))
            self.image_tk_c = IT.PhotoImage(self.res_c)
            self.ID_L.config(image=self.image_tk_c)
            self.Qrcode.clear()


            self.message = 'Done'
            self.message_L.config(text=self.message, fg='green')

            self.ID.set('')
            self.Fname.set('')
            self.position.set('')
            self.department.set('')
            self.E3.current(0)
            self.E4.current(0)
            self.message_L.config(text=self.message, fg='green')
            self.signature_canvas.delete("all")
            self.signature_drawn = False

            self.B4.config(state='normal')

    def clear(self):
        self.ID.set('')
        self.Fname.set('')
        self.position.set('')
        self.department.set('')
        self.E3.current(0)
        self.E4.current(0)
        self.message_L.config(text=self.message, fg='green')
        self.signature_canvas.delete("all")
        self.signature_drawn = False
        self.ID_L.config(image='')

    def next(self):
        # Close the current Tkinter window
        self.root.destroy()
        subprocess.Popen(['python', 'faculty_back.py'])


root = Tk()
App = Win(root)
root.mainloop()
