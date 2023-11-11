import subprocess
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import Tk, Entry, StringVar
from PIL import Image as I
from PIL import ImageTk as IT
from PIL import ImageDraw as ID
from PIL import ImageFont as IF
from datetime import datetime
import qrcode as Q
from resizeimage import resizeimage as re
import barcode2d
import win32print
import win32ui
import win32con
import tkinter.messagebox as messagebox
import os
from pdf417 import encode, render_image
import re as RE


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
        bg_image = I.open('maroon.png')
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
        self.L1 = Label(self.F1, text='DATE OF ID CREATION', font=F3, bg='#B29999').place(x=10, y=60)
        self.L2 = Label(self.F1, text='ID NO.', font=F3, bg='#B29999').place(x=335, y=60)
        self.L3 = Label(self.F1, text='GSIS NO.', font=F3, bg='#B29999').place(x=10, y=115)
        self.L4 = Label(self.F1, text='GSIS BP NO.', font=F3, bg='#B29999').place(x=310, y=115)
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

        initial_text = "TUPC-ID NO. #### "

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

        self.E1 = Entry(self.F1, font=F3, textvariable=self.DATE)
        self.E1.place(x=210, y=60, width=120)
        self.E1.insert(0, "mm-dd-yyyy")  # Placeholder text
        self.E1.config(fg="gray")  # Set text color to gray
        self.E1.bind("<FocusIn>", self.on_entry_click_date)
        self.E1.bind("<FocusOut>", self.on_focus_out_date)

        # Entry for ID
        self.E2 = Entry(self.F1, font=F3, textvariable=self.ID)
        self.E2.place(x=420, y=60, width=200)
        self.E2.insert(0, initial_text)
        self.E2.config(fg="gray")
        self.E2.bind("<FocusIn>", self.on_entry_click)
        self.E2.bind("<FocusOut>", self.on_focus_out)

        self.E3 = Entry(self.F1, font=F3, textvariable=self.GSIS)
        self.E3.place(x=100, y=115, width=200)
        self.E3['validate'] = 'key'
        self.E3['validatecommand'] = (self.E3.register(self.on_validate_numbers), '%P')

        self.E4 = Entry(self.F1, font=F3, textvariable=self.POLICY)
        self.E4.place(x=420, y=115, width=200)
        self.E4['validate'] = 'key'
        self.E4['validatecommand'] = (self.E4.register(self.on_validate_numbers), '%P')

        self.E5 = Entry(self.F1, font=F3, textvariable=self.TIN)
        self.E5.place(x=100, y=155, width=200)
        self.E5['validate'] = 'key'
        self.E5['validatecommand'] = (self.E5.register(self.on_validate_numbers), '%P')

        self.E6 = Entry(self.F1, font=F3, textvariable=self.PAGIBIG)
        self.E6.place(x=420, y=155, width=200)
        self.E6['validate'] = 'key'
        self.E6['validatecommand'] = (self.E6.register(self.on_validate_numbers), '%P')

        self.E7 = Entry(self.F1, font=F3, textvariable=self.PHILHEALTH)
        self.E7.place(x=180, y=195, width=400)
        self.E7['validate'] = 'key'
        self.E7['validatecommand'] = (self.E7.register(self.on_validate_numbers), '%P')

        self.E8 = Entry(self.F1, font=F3, textvariable=self.FNAME).place(x=208, y=270, width=400)
        self.E9 = Entry(self.F1, font=F3, textvariable=self.STREET).place(x=208, y=300, width=400)
        self.E10 = Entry(self.F1, font=F3, textvariable=self.BRGY).place(x=208, y=330, width=400)
        self.E11 = Entry(self.F1, font=F3, textvariable=self.CITY).place(x=208, y=360, width=400)
        self.E12 = Entry(self.F1, font=F3, textvariable=self.CONTACT)
        self.E12.place(x=208, y=390, width=400)
        self.E12['validate'] = 'key'
        self.E12['validatecommand'] = (self.E12.register(self.on_validate_contact), '%P')

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
        self.ID_Frame = Frame(self.F2, relief=SUNKEN)
        self.ID_Frame.place(x=200, y=100, width=255, height=380)

        self.ID_L = Label(self.ID_Frame, text='ID\nCard\nNot Found', font=F1, bg='#B29999')
        self.ID_L.place(x=0, y=0, relwidth=1, relheight=1)

    def on_entry_click(self, event):
        current_text = self.E2.get()
        if current_text == "TUPC-ID NO. #### ":
            self.E2.delete(0, "end")  # Delete the current text
            self.E2.insert(0, "TUPC-ID NO. ")  # Set the initial format
            self.E2.icursor(11)  # Set the cursor position after "TUPC-ID NO. "
            self.E2.config(fg="black")
            self.E2.bind("<Key>", self.on_key_press)  # Bind the Key event

    def on_key_press(self, event):
        # Allow only numbers and '-' character
        allowed_chars = set("0123456789-")

        if event.char == "" or event.char in allowed_chars:
            # If BackSpace or allowed character, proceed with the default behavior
            return

        # If other keys are pressed, check the position of the cursor
        cursor_position = self.E2.index(INSERT)
        if cursor_position <= 11:
            # If the cursor is at or before the "TUPC-ID NO.", prevent modifications
            return 'break'

        # If the cursor is after the "TUPC-ID NO.", allow modifications
        return

    def on_focus_out(self, event):
        current_text = self.E2.get()
        if current_text == "TUPC-ID NO. ":
            # Reset to the placeholder
            self.E2.delete(0, "end")
            self.E2.insert(0, "TUPC-ID NO. #### ")
            self.E2.config(fg="gray")
            self.E2.unbind("<Key>")  # Unbind the Key event
        elif not RE.match(r'^TUPC-ID NO. \d{2}-\d{3}$', current_text):
            # If the entered text doesn't match the specified format, do not reset
            return
        else:
            # Text matches the expected format, keep it as is
            return

    def on_entry_click_date(self, event):
        if self.E1.get() == "mm-dd-yyyy":
            self.E1.delete(0, "end")
            self.E1.config(fg="black")

    def on_focus_out_date(self, event):
        if self.E1.get() == "":
            self.E1.insert(0, "mm-dd-yyyy")
            self.E1.config(fg="gray")

    def on_validate_contact(self, P):
        # P is the proposed text
        return P.isdigit() and len(P) <= 11

    def on_validate_numbers(self, P):
        # P is the proposed text
        return all(char.isdigit() or char == '-' for char in P)


    def generate_barcode_image(self, barcode_value):
        # Encode the barcode data with fewer columns (e.g., 4 columns)
        barcode_data = encode(barcode_value, columns=4)

        # Generate the barcode image
        barcode_image = render_image(barcode_data)

        # Resize the barcode image
        barcode_image = barcode_image.resize((586, 221))

        return barcode_image

    def is_valid_date_format(self, date_str):
        try:
            # Attempt to parse the date string
            datetime.strptime(date_str, '%m-%d-%Y')
            return True
        except ValueError:
            return False

    def generate(self):
        contact_no = self.CONTACT.get()

        # Check if contact_no contains only digits and has a length of 11
        if not contact_no.isdigit() or len(contact_no) != 11:
            self.message = 'Contact number must be exactly 11 digits and contain only numbers.'
            self.message_L.config(text=self.message, fg='red')

        # Check if E2 is still equal to the placeholder or only contains the word 'TUPC-ID NO.'
        if self.E2.get() == "TUPC-ID NO. #### " or not RE.match(r'^TUPC-ID NO.\d{2}-\d{3}$', self.E2.get()):
            self.message = 'Please enter a valid ID number.'
            self.message_L.config(text=self.message, fg='red')

        # Check if the date entered in E1 matches the specified format
        elif not self.is_valid_date_format(self.DATE.get()):
            self.message = 'Please enter a valid date format (mm-dd-yyyy).'
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
            self.Draw.text((106, 135), self.FNAME.get(), fill='black', font=font, anchor='mm')
            self.Draw.text((107, 155), self.STREET.get(), fill='black', font=font1, anchor='mm')
            self.Draw.text((105, 170), self.BRGY.get(), fill='black', font=font1, anchor='mm')
            self.Draw.text((107, 185), self.CITY.get(), fill='black', font=font1, anchor='mm')
            self.Draw.text((70, 198 ), self.CONTACT.get(), fill='black', font=font)


            # Rotate the department text before pasting it onto the ID card
            date_text = self.DATE.get()
            date_font = IF.truetype(font='Arial Bold.ttf', size=8)
            date_font_image = I.new('RGBA', (48, 16), 'white')  # Create a transparent image
            date_draw = ID.Draw(date_font_image)
            date_draw.text((2, 0), date_text, fill='black', font=date_font)

            # Rotate the text by the desired angle (e.g., 45 degrees)
            rotated_date_font_image = date_font_image.rotate(90, expand=True)

            # Paste the rotated department text onto the ID card image
            self.image_c.paste(rotated_date_font_image,
                               (191, 277))  # Adjust x and y positions as needed


            # Generate a PDF417 barcode
            barcode_value = self.ID.get()

            # Generate the barcode image using the new method
            barcode_image = self.generate_barcode_image(barcode_value)

            # Save the barcode image to a file
            barcode_filename = 'BARCODE_FACULTY/' + barcode_value + '.png'
            barcode_image.save(barcode_filename)
            barcode_img = I.open(barcode_filename)

            cropped_barcode_img = barcode_img.crop((0, 40, barcode_img.width - 10, barcode_img.height - 32))

            # Resize the cropped barcode image
            cropped_barcode_img = cropped_barcode_img.resize((82, 44))

            # Paste the barcode image onto the ID card
            self.image_c.paste(cropped_barcode_img, (104, 280))  # Adjust the coordinates for proper placement

            # Save the final ID card image
            self.image_c.save('FACULTY_BACK/ID_' + str(self.ID.get()) + '.png')
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
