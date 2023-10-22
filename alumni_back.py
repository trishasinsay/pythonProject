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
        self.L1 = Label(self.F1, text='STUDENT ID NUMBER', font=F3, bg='#B29999').place(x=10, y=100)
        self.L2 = Label(self.F1, text='SIGNATURE', font=F3, bg='#B29999').place(x=10, y=150)

        self.ID = StringVar()

        self.E1 = Entry(self.F1, font=F3, textvariable=self.ID).place(x=210, y=100, width=400)


        # BUTTON
        self.B1 = Button(self.F1, text='Generate', font=F2, command=self.generate)
        self.B1.place(x=50, y=450, width=200)

        self.B2 = Button(self.F1, text='Clear', font=F2, command=self.clear)
        self.B2.place(x=380, y=450, width=200)

        self.B3 = Button(self.root, text='Next', font=F2, command=self.next, bg='#5D1C1C', fg='white', state='disabled')
        self.B3.place(x=1130, y=620, width=200)

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
        self.signature_canvas.place(x=20, y=200, width=600, height=180)

        # Bind mouse events to the canvas
        self.signature_canvas.bind("<Button-1>", self.start_drawing)
        self.signature_canvas.bind("<B1-Motion>", self.draw)
        self.signature_canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.signature_drawn = False

        # F2
        self.ID_Frame = Frame(self.F2, relief=SUNKEN, bd=1)
        self.ID_Frame.place(x=150, y=220, width=327, height=205)

        self.ID_L = Label(self.ID_Frame, text='ID\nCard\nNot Found', font=F1)
        self.ID_L.place(x=0, y=0, relwidth=1, relheight=1)


    def start_drawing(self, event):
        self.is_drawing = True
        self.last_x = event.x
        self.last_y = event.y
        self.signature_coords = []  # Start with an empty list for new signature

    def draw(self, event):
        if self.is_drawing:
            self.signature_canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill='black', width=2)
            self.last_x = event.x
            self.last_y = event.y
            self.signature_coords.append((event.x, event.y))  # Store coordinates

    def stop_drawing(self, event):
        self.is_drawing = False
        self.signature_drawn = True


    def remove_background(self, image):
        # Convert the image to grayscale
        image_gray = ImageOps.grayscale(image)

        # Create a binary mask by applying a threshold
        threshold = 500  # Adjust the threshold value as needed
        mask = image_gray.point(lambda p: p < threshold and 255)

        # Optionally, you can apply a filter to the mask to refine it (e.g., remove noise)
        mask = mask.filter(ImageFilter.MedianFilter(size=5))

        # Make the image RGBA
        image_rgba = image.convert('RGBA')

        # Apply the mask to the image
        signature_image = ImageChops.composite(image_rgba, Image.new('RGBA', image.size, (255, 255, 255, 0)), mask)

        return signature_image

    def generate(self):
        if self.ID.get() == '' :
            self.message = 'Please input your ID number'
            self.message_L.config(text=self.message, fg='red')
            self.B3.config(state='disabled')


        elif not self.signature_drawn:
            self.message = 'Please provide a signature'
            self.message_L.config(text=self.message, fg='red')
            self.B3.config(state='disabled')

        else:

            background_image = I.open('alumni.png')
            background_image = background_image.resize((327, 205))

            self.image_c = background_image.copy()
            self.Draw = ID.Draw(self.image_c)

            # Save the drawn signature as an image
            signature_filename = f'signatures/signature_{self.ID.get()}.png'
            self.signature_canvas.postscript(file=signature_filename, colormode='color')

            # Load the saved signature image and remove the background
            if os.path.exists(signature_filename):
                signature_image = I.open(signature_filename)
                signature_image = signature_image.convert('RGBA')
                signature_image = self.remove_background(signature_image)

                # Resize the signature image to the desired size
                new_signature_size = (180, 29)  # Adjust the size as needed
                signature_image = signature_image.resize(new_signature_size)

                # Paste the signature image onto the ID card
                self.image_c.paste(signature_image, (71, 10))  # Adjust the position as needed


            self.image_c.save('ALUMBACK\ID_' + str(self.ID.get()) + '.png')
            self.res_c = self.image_c.resize((327, 205))
            self.image_tk_c = IT.PhotoImage(self.res_c)
            self.ID_L.config(image=self.image_tk_c)


            self.message = 'Done'
            self.message_L.config(text=self.message, fg='green')

            self.ID.set('')
            self.message_L.config(text=self.message, fg='green')
            self.signature_canvas.delete("all")
            self.signature_drawn = False

            self.B3.config(state='normal')

    def clear(self):
        self.ID.set('')
        self.message_L.config(text=self.message, fg='green')
        self.signature_canvas.delete("all")
        self.signature_drawn = False
        self.ID_L.config(image='')

    def next(self):
        # Close the current Tkinter window
        self.root.destroy()
        subprocess.Popen(['python', 'id_back.py'])


root = Tk()
App = Win(root)
root.mainloop()
