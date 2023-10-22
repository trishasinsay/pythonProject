from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image as I
from PIL import ImageTk as IT
from PIL import ImageDraw as ID
from PIL import ImageFont as IF
import qrcode as Q
from resizeimage import resizeimage as re
import barcode
from barcode.writer import ImageWriter
import win32print
import win32ui
import win32con
import tkinter.messagebox as messagebox
import os
from pdf417gen import encode
from barcode import generate

# WIN SETTINGS
title = 'TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES - CAVITE CAMPUS KIOSK ID MAKER'
size = '1366x768'
icon = ''
res = 0
W = [title, size, res, icon]

# FONTS
F1 = ('cambria', 23)
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
        bg_image = I.open('req_bg.png')
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
        self.L1 = Label(self.F1, text='DATE', font=F3, bg='#B29999').place(x=10, y=60)
        self.L2 = Label(self.F1, text='ID NO.', font=F3, bg='#B29999').place(x=335, y=60)
        self.L3 = Label(self.F1, text='GSIS NO.', font=F3, bg='#B29999').place(x=10, y=115)
        self.L4 = Label(self.F1, text='POLICY NO.', font=F3, bg='#B29999').place(x=310, y=115)
        self.L5 = Label(self.F1, text='TIN NO.', font=F3, bg='#B29999').place(x=10, y=155)
        self.L6 = Label(self.F1, text='PAG-IBIG NO.', font=F3, bg='#B29999').place(x=300, y=155)
        self.L7 = Label(self.F1, text='PHILHEALTH NO.', font=F3, bg='#B29999').place(x=10, y=195)
        self.L8 = Label(self.F1, text='IN CASE OF EMERGENCY, CONTACT:', font=F3, bg='#B29999').place(x=10, y=235)
        self.L9 = Label(self.F1, text='FULL NAME', font=F3, bg='#B29999').place(x=10, y=270)
        self.L10 = Label(self.F1, text='HOUSE NO. & STREET', font=F3, bg='#B29999').place(x=10, y=300)
        self.L11 = Label(self.F1, text='BARANGAY', font=F3, bg='#B29999').place(x=10, y=330)
        self.L12 = Label(self.F1, text='CITY & PROVINCE', font=F3, bg='#B29999').place(x=10, y=360)
        self.L13 = Label(self.F1, text='CONTACT NO.', font=F3, bg='#B29999').place(x=10, y=390)
        self.L14 = Label(self.F1, text='*Note: Please answer all fields honestly and check your information before\npressing "Next" button and Use CAPITAL LETTERS only', font=F4, bg='#B29999')
        self.L14.place(x=120, y=430)
        self.L15 = Label(self.F1,text='*Note: When you are capturing image, press the ENTER KEY to capture your image',font=F4, bg='#B29999')
        self.L15.place(x=90, y=460)
        self.L16 = Label(self.F1, text='Date Format: mm-dd-yyyy',
                         font=F4, bg='#B29999')
        self.L16.place(x=120, y=85)
        self.L16 = Label(self.F1, text='Format: TUPC-ID NO. ####',
                         font=F4, bg='#B29999')
        self.L16.place(x=440, y=85)


        self.ID = StringVar()
        self.DATE = StringVar()
        self.GSIS = StringVar()
        self.POLICY = StringVar()
        self.TIN = StringVar()
        self.PAGIBIG = StringVar()
        self.PHILHEALTH = StringVar()
        self.FNAME = StringVar()
        self.STREET = StringVar()
        self.BRGY = StringVar()
        self.CITY = StringVar()
        self.CONTACT = StringVar()

        self.E1 = Entry(self.F1, font=F3, textvariable=self.DATE).place(x=100, y=60, width=200)
        self.E2 = Entry(self.F1, font=F3, textvariable=self.ID).place(x=420, y=60, width=200)
        self.E3 = Entry(self.F1, font=F3, textvariable=self.GSIS).place(x=100, y=115, width=200)
        self.E4 = Entry(self.F1, font=F3, textvariable=self.POLICY).place(x=420, y=115, width=200)
        self.E5 = Entry(self.F1, font=F3, textvariable=self.TIN).place(x=100, y=155, width=200)
        self.E6 = Entry(self.F1, font=F3, textvariable=self.PAGIBIG).place(x=420, y=155, width=200)
        self.E7 = Entry(self.F1, font=F3, textvariable=self.PHILHEALTH).place(x=180, y=195, width=400)
        self.E8 = Entry(self.F1, font=F3, textvariable=self.FNAME).place(x=208, y=270, width=400)
        self.E9 = Entry(self.F1, font=F3, textvariable=self.STREET).place(x=208, y=300, width=400)
        self.E10 = Entry(self.F1, font=F3, textvariable=self.BRGY).place(x=208, y=330, width=400)
        self.E11 = Entry(self.F1, font=F3, textvariable=self.CITY).place(x=208, y=360, width=400)
        self.E12 = Entry(self.F1, font=F3, textvariable=self.CONTACT).place(x=208, y=390, width=400)

        # BUTTON
        self.B1 = Button(self.F1, text='Generate', font=F2, command=self.generate)
        self.B1.place(x=20, y=490, width=180)

        self.B2 = Button(self.F1, text='Clear', font=F2, command=self.clear)
        self.B2.place(x=430, y=490, width=180)

        self.B3 = Button(self.root, text='PRINT', font=F2, command=self.next, bg='#5D1C1C', fg='white', state='disabled')
        self.B3.place(x=1130, y=620, width=200)

        # MESSAGE BOX
        self.message = ''
        self.message_F = Frame(self.F1, relief=SUNKEN, bd=1)
        self.message_F.place(x=15, y=550, width=600, height=30)

        self.message_L = Label(self.message_F, text=self.message, font=F3, bd=1)
        self.message_L.place(x=0, y=0, relwidth=1, relheight=1)

        # F2
        self.ID_Frame = Frame(self.F2, relief=SUNKEN, bd=1)
        self.ID_Frame.place(x=200, y=100, width=255, height=380)

        self.ID_L = Label(self.ID_Frame, text='ID\nCard\nNot Found', font=F1)
        self.ID_L.place(x=0, y=0, relwidth=1, relheight=1)


    def generate(self):
        contact_no = self.CONTACT.get()

        # Check if contact_no contains only digits and has a length of 11
        if not contact_no.isdigit() or len(contact_no) != 11:
            self.message = 'Contact number must be exactly 11 digits and contain only numbers.'
            self.message_L.config(text=self.message, fg='red')

        elif (self.ID.get() == '' or self.DATE.get() == '' or self.GSIS.get() == '' or self.POLICY.get() == ''
                or self.TIN.get() == '' or self.PAGIBIG.get() == '' or self.PHILHEALTH.get() == '' or self.FNAME.get() == '') \
                or self.STREET.get() == '' or self.BRGY.get() == '' or self.CITY.get() == '' or self.CONTACT.get() == '':

            self.message = 'Please answer all input fields'
            self.message_L.config(text=self.message, fg='red')
            self.B3.config(state='disabled')

        else:
            font = IF.truetype(font='Arial Bold.ttf', size=10)
            font1 = IF.truetype(font='arial.ttf', size=10)
            font2 = IF.truetype(font='Arial Bold.ttf', size=7)

            background_image = I.open('faculty_back.png')
            background_image = background_image.resize((205, 327))

            self.image_c = background_image.copy()
            self.Draw = ID.Draw(self.image_c)

            angle = 270
            self.Draw.text((96, 9), self.GSIS.get(), fill='black', font=font1)
            self.Draw.text((96, 27), self.POLICY.get(), fill='black', font=font1)
            self.Draw.text((96, 44), self.TIN.get(), fill='black', font=font1)
            self.Draw.text((96, 61), self.PAGIBIG.get(), fill='black', font=font1)
            self.Draw.text((96, 78), self.PHILHEALTH.get(), fill='black', font=font1)
            self.Draw.text((35, 127), self.FNAME.get(), fill='black', font=font)
            self.Draw.text((35, 147 ), self.STREET.get(), fill='black', font=font1)
            self.Draw.text((65, 165), self.BRGY.get(), fill='black', font=font1)
            self.Draw.text((55, 180 ), self.CITY.get(), fill='black', font=font1)
            self.Draw.text((70, 198 ), self.CONTACT.get(), fill='black', font=font)
            self.Draw.text((156, 290 ), self.DATE.get(), fill='black', font=font2)

            # Generate a PDF417 barcode
            barcode_value = self.ID.get()

            # Encode the barcode data
            barcode_data = encode(barcode_value, columns=4)

            # Generate the barcode image
            barcode_image = self.generate_barcode_image(barcode_data)

            # Save the barcode image to a file
            barcode_image.save('Barcode/' + barcode_value + '.png')

            # Crop the barcode image (adjust cropping values as needed)
            # Note: PDF417 barcodes are usually more rectangular, so cropping may vary
            cropped_barcode_img = barcode_image.crop((0, 0, barcode_image.width, barcode_image.height - 73))

            # Resize the cropped barcode image
            cropped_barcode_img = cropped_barcode_img.resize((84, 43))

            # Paste the cropped barcode image onto the ID card
            self.image_c.paste(cropped_barcode_img, (105, 276))

            self.image_c.save('FACULTY BARCODE\ID_' + str(self.ID.get()) + '.png')
            self.res_c = self.image_c.resize((255, 380))
            self.image_tk_c = IT.PhotoImage(self.res_c)
            self.ID_L.config(image=self.image_tk_c)
            self.message = 'Done'
            self.message_L.config(text=self.message, fg='green')

            self.ID.set('')
            self.GSIS.set('')
            self.POLICY.set('')
            self.TIN.set('')
            self.PAGIBIG.set('')
            self.PHILHEALTH.set('')
            self.FNAME.set('')
            self.STREET.set('')
            self.BRGY.set('')
            self.CITY.set('')
            self.CONTACT.set('')
            self.DATE.set('')
            self.message_L.config(text=self.message, fg='green')

    def generate_barcode_image(self, barcode_data):
        # Define the size and scale for the barcode image
        width = 200
        height = 100
        scale = 4

        # Create a blank image with white background
        image = I.new('RGB', (width, height), 'white')
        draw = ID.Draw(image)

        # Calculate the number of rows and columns
        num_rows = len(barcode_data)
        num_cols = len(barcode_data[0])

        # Calculate the width and height of each cell
        cell_width = width // num_cols
        cell_height = height // num_rows

        # Iterate through the barcode data and draw black squares for filled cells
        for row in range(num_rows):
            for col in range(num_cols):
                if barcode_data[row][col] == 1:
                    x0 = col * cell_width
                    y0 = row * cell_height
                    x1 = (col + 1) * cell_width
                    y1 = (row + 1) * cell_height
                    draw.rectangle([x0, y0, x1, y1], fill='black')

        # Resize the barcode image
        barcode_image = image.resize((width * scale, height * scale))

        return barcode_image
    def clear(self):
        self.ID.set('')
        self.GSIS.set('')
        self.POLICY.set('')
        self.TIN.set('')
        self.PAGIBIG.set('')
        self.PHILHEALTH.set('')
        self.FNAME.set('')
        self.STREET.set('')
        self.BRGY.set('')
        self.CITY.set('')
        self.CONTACT.set('')
        self.DATE.set('')
        self.message_L.config(text=self.message, fg='green')
        self.ID_L.config(image='')

    def next(self):
        # Close the current Tkinter window
        self.root.destroy()
        subprocess.Popen(['python', 'id_back.py'])


root = Tk()
App = Win(root)
root.mainloop()
