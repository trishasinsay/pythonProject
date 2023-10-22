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

        # Load the background image
        bg_image = Image.open('req_bg.png')
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
        self.L1 = Label(self.F1, text='STUDENT ID NUMBER', font=F3, bg='#B29999').place(x=10, y=60)
        self.L2 = Label(self.F1, text='FIRST NAME & M.I.', font=F3, bg='#B29999').place(x=10, y=100)
        self.L3 = Label(self.F1, text='LAST NAME', font=F3, bg='#B29999').place(x=10, y=140)
        self.L4 = Label(self.F1, text='PROGRAM', font=F3, bg='#B29999').place(x=10, y=180)
        self.L5 = Label(self.F1, text='YEAR GRADUATED', font=F3, bg='#B29999').place(x=10, y=220)
        self.L6 = Label(self.F1, text='TIN', font=F3, bg='#B29999').place(x=10, y=260)
        self.L7 = Label(self.F1, text='SSS/GSIS NO.', font=F3, bg='#B29999').place(x=10, y=310)
        self.L8 = Label(self.F1, text='*Note: Please answer all fields honestly and check your information before\npressing "Next" button and Use CAPITAL LETTERS only', font=F4, bg='#B29999')
        self.L8.place(x=120, y=350)
        self.L9 = Label(self.F1,text='*Note: When you are capturing image, press the ENTER KEY to capture your image',font=F4, bg='#B29999')
        self.L9.place(x=90, y=385)

        self.ID = StringVar()
        self.Fname = StringVar()
        self.Lname = StringVar()
        self.program = StringVar()
        self.graduated = StringVar()
        self.tin = StringVar()
        self.gsis = StringVar()

        self.E1 = Entry(self.F1, font=F3, textvariable=self.ID).place(x=210, y=60, width=400)
        self.E2 = Entry(self.F1, font=F3, textvariable=self.Fname).place(x=208, y=100, width=400)
        self.E3 = Entry(self.F1, font=F3, textvariable=self.Lname).place(x=208, y=140, width=400)
        self.E4 = ttk.Combobox(self.F1, font=F3, state='readonly', textvariable=self.program)
        self.E4['values'] = ("Select your Program",
                             "BSCE", "BSEE", 'BSME', 'BSIE-ICT', "BSIE-HE", "BSIE-IA", "BTTE-CP",
                             "BTTE-EI", "BTTE-AU", "BTTE-HVACT", "BTTE-E", "BGT-AT", "BET-CT",
                             "BET-ET", "BET-ESET", "BET-COET", "BET-MT", "BET-PPT", "BET-AT")
        self.E4.current(0)
        self.E4.place(x=208, y=180, width=400)
        self.E5 = Entry(self.F1, font=F3, textvariable=self.graduated).place(x=208, y=220, width=400)
        self.E6 = Entry(self.F1, font=F3, textvariable=self.tin).place(x=208, y=260, width=400)
        self.E7 = Entry(self.F1, font=F3, textvariable=self.gsis).place(x=208, y=310, width=400)


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


        # F2
        self.ID_Frame = Frame(self.F2, relief=SUNKEN, bd=1)
        self.ID_Frame.place(x=150, y=200, width=327, height=205)

        self.ID_L = Label(self.ID_Frame, text='ID\nCard\nNot Found', font=F1)
        self.ID_L.place(x=0, y=0, relwidth=1, relheight=1)


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
            resized_photo = cv2.resize(self.captured_photo, (85, 76))

            # Save the processed photo
            processed_photo_filename = f'processed_photos/photo_{current_time}.jpg'
            cv2.imwrite(processed_photo_filename, resized_photo)



    def generate(self):
        if self.ID.get() == '' or self.Fname.get() == '' or self.Lname.get() == '' or self.program.get() == ''\
                or self.graduated.get() == '' or self.tin.get() == '' or self.gsis.get() == '':
            self.message = 'Please answer all input fields'
            self.message_L.config(text=self.message, fg='red')
            self.B4.config(state='disabled')

        elif self.E4.current() == 0:
            self.message = 'Please select your program'
            self.message_L.config(text=self.message, fg='red')
            self.B4.config(state='disabled')

        elif not hasattr(self, 'captured_photo'):
            self.message = 'Please capture your photo'
            self.message_L.config(text=self.message, fg='red')
            self.B4.config(state='disabled')


        else:
            font1 = IF.truetype(font='Arial Bold.ttf', size=10)
            font2 = IF.truetype(font='arial.ttf', size=7)


            background_image = I.open('alumni_front.png')
            background_image = background_image.resize((327, 205))

            self.image_c = background_image.copy()
            self.Draw = ID.Draw(self.image_c)

            self.Draw.text((92, 75), self.Lname.get(), fill='black', font=font1)
            self.Draw.text((92, 85), self.Fname.get(), fill='black', font=font1)
            self.Draw.text((138, 106), self.ID.get(), fill='black', font=font2)
            self.Draw.text((151, 115), self.program.get(), fill='black', font=font2)
            self.Draw.text((165, 124), self.graduated.get(), fill='black', font=font2)
            self.Draw.text((135, 133), self.tin.get(), fill='black', font=font2)
            self.Draw.text((158, 141), self.gsis.get(), fill='black', font=font2)

            # Load the captured image
            if hasattr(self, 'captured_photo'):
                # Process the captured photo and paste it onto the ID card
                resized_photo = cv2.resize(self.captured_photo, (85, 76))  # Adjust the size as needed
                photo_paste = I.fromarray(cv2.cvtColor(resized_photo, cv2.COLOR_BGR2RGB))
                self.image_c.paste(photo_paste, (5, 75))  # Adjust the position as needed

            self.image_c.save('ALUMNI\ID_' + str(self.ID.get()) + '.png')
            self.res_c = self.image_c.resize((327, 205))
            self.image_tk_c = IT.PhotoImage(self.res_c)
            self.ID_L.config(image=self.image_tk_c)


            self.message = 'Done'
            self.message_L.config(text=self.message, fg='green')

            self.ID.set('')
            self.Fname.set('')
            self.Lname.set('')
            self.program.set('')
            self.E4.current(0)
            self.graduated.set('')
            self.tin.set('')
            self.gsis.set('')
            self.message_L.config(text=self.message, fg='green')

            self.B4.config(state='normal')

    def clear(self):
        self.ID.set('')
        self.Fname.set('')
        self.Lname.set('')
        self.program.set('')
        self.E4.current(0)
        self.graduated.set('')
        self.tin.set('')
        self.gsis.set('')
        self.message_L.config(text=self.message, fg='green')
        self.ID_L.config(image='')

    def next(self):
        # Close the current Tkinter window
        self.root.destroy()
        subprocess.Popen(['python', 'alumni_back.py'])


root = Tk()
App = Win(root)
root.mainloop()
