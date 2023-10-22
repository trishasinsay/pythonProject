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
from barcode import Code39
from barcode.writer import ImageWriter
import win32print
import win32ui
import win32con
import tkinter.messagebox as messagebox
import os


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
        self.F2.pack(side='right', padx=20, pady=20, fill='both',
                     expand=True)  # Expand both horizontally and vertically

        self.F1_title = Label(self.F1, bg='black', fg='#FFFFFF', text='Personal Details', font=F1)
        self.F1_title.place(x=0, y=0, relwidth=1)

        self.F2_title = Label(self.F2, bg='black', fg='#FFFFFF', text='ID Preview', font=F1)
        self.F2_title.place(x=0, y=0, relwidth=1)

        # LABELS
        self.L1 = Label(self.F1, text='STUDENT ID NUMBER', font=F3, bg='#B29999').place(x=10, y=70)
        self.L2 = Label(self.F1, text='INCASE OF EMERGENCY, CONTACT:', font=F3, bg='#B29999').place(x=10, y=130)
        self.L3 = Label(self.F1, text='FULL NAME', font=F3, bg='#B29999').place(x=10, y=185)
        self.L4 = Label(self.F1, text='CONTACT NO.', font=F3, bg='#B29999').place(x=10, y=220)
        self.L5 = Label(self.F1, text='HOUSE NO. & STREET', font=F3, bg='#B29999').place(x=10, y=255)
        self.L6 = Label(self.F1, text='BARANGAY', font=F3, bg='#B29999').place(x=10, y=290)
        self.L7 = Label(self.F1, text='CITY & PROVINCE', font=F3, bg='#B29999').place(x=10, y=325)
        self.L8 = Label(self.F1,
                        text='*Note: Please answer all fields honestly and check your information before\npressing "Next" button and Use CAPITAL LETTERS only',
                        font=F4, bg='#B29999').place(x=120, y=380)

        self.ID = StringVar()
        self.C_name = StringVar()
        self.C_no = StringVar()
        self.C_street = StringVar()
        self.C_barangay = StringVar()
        self.C_city = StringVar()


        self.E1 = Entry(self.F1, font=F3, textvariable=self.ID).place(x=208, y=70, width=400)
        self.E2 = Entry(self.F1, font=F3, textvariable=self.C_name).place(x=208, y=185, width=400)
        self.E3 = Entry(self.F1, font=F3, textvariable=self.C_no).place(x=208, y=220, width=400)
        self.E4 = Entry(self.F1, font=F3, textvariable=self.C_street).place(x=208, y=255, width=400)
        self.E5 = Entry(self.F1, font=F3, textvariable=self.C_barangay).place(x=208, y=290, width=400)
        self.E5 = Entry(self.F1, font=F3, textvariable=self.C_city).place(x=208, y=325, width=400)


        # BUTTON
        self.B1 = Button(self.F1, text='Generate', font=F2, command=self.generate)
        self.B1.place(x=30, y=470, width=250)

        self.B2 = Button(self.F1, text='Clear', font=F2, command=self.clear)
        self.B2.place(x=350, y=470, width=250)

        self.B3 = Button(self.root, text='Print', font=F2, command=self.print_id, bg='#5D1C1C', fg='white')
        self.B3.place(x=1130, y=620, width=200)

        # MESSAGE BOX
        self.message = ''
        self.message_F = Frame(self.F1, relief=SUNKEN, bd=1)
        self.message_F.place(x=15, y=540, width=600, height=40)

        self.message_L = Label(self.message_F, text=self.message, font=F3, bd=1)
        self.message_L.place(x=0, y=0, relwidth=1, relheight=1)

        # F2
        self.ID_Frame_Back = Frame(self.F2, relief=SUNKEN, bd=1)
        self.ID_Frame_Back.place(x=200, y=100, width=255, height=380)

        self.ID_L = Label(self.ID_Frame_Back, text='ID\nCard\nNot Found', font=F1)
        self.ID_L.place(x=0, y=0, relwidth=1, relheight=1)


    def generate(self):
        contact_no = self.C_no.get()

        # Check if contact_no contains only digits and has a length of 11
        if not contact_no.isdigit() or len(contact_no) != 11:
            self.message = 'Contact number must be exactly 11 digits and contain only numbers.'
            self.message_L.config(text=self.message, fg='red')

        elif self.ID.get() == '' or self.C_name.get() == '' or self.C_street.get() == '' or self.C_barangay.get() == '' or self.C_city.get() == '':
            self.message = 'Please answer all input fields'
            self.message_L.config(text=self.message, fg='red')

        else:
            font1 = IF.truetype(font='Arial Bold.ttf', size=7)
            font2 = IF.truetype(font='arial.ttf', size=7)
            font4 = IF.truetype(font='Arial Bold.ttf', size=8)
            font5 = IF.truetype(font='arial.ttf', size=8)

            background_image = I.open('back_template.png')
            background_image = background_image.resize((205, 327))

            self.image_c = background_image.copy()
            self.Draw = ID.Draw(self.image_c)


            self.Draw.text((50, 78), self.C_name.get(), fill='black', font=font4)
            self.Draw.text((30, 100), self.C_street.get(), fill='black', font=font2)
            self.Draw.text((65, 110), self.C_barangay.get(), fill='black', font=font2)
            self.Draw.text((62, 120), self.C_city.get(), fill='black', font=font2)
            self.Draw.text((75, 139), self.C_no.get(), fill='black', font=font5)


            # Generate a barcode
            barcode_value = self.ID.get()
            code = Code39(barcode_value, writer=ImageWriter(), add_checksum=False)
            barcode_image = code.save(f'Barcode\ {barcode_value}', options={"module_width": 0.2, "module_height": 10})

            barcode_img = I.open(barcode_image)

            # Crop the barcode image to remove the human-readable text (adjust cropping values as needed)
            cropped_barcode_img = barcode_img.crop((0, 0, barcode_img.width, barcode_img.height - 73))

            # Resize the cropped barcode image
            cropped_barcode_img = cropped_barcode_img.resize((185, 35))

            # Paste the cropped barcode image onto the ID card
            self.image_c.paste(cropped_barcode_img, (14, 286))

            self.image_c.save('Library\ID_' + str(self.ID.get()) + '.png')
            self.res_c = self.image_c.resize((255, 380))
            self.image_tk_c = IT.PhotoImage(self.res_c)
            self.ID_L.config(image=self.image_tk_c)
            self.message = 'Done'
            self.message_L.config(text=self.message, fg='green')

            self.ID.set('')
            self.C_name.set('')
            self.C_no.set('')
            self.C_street.set('')
            self.C_barangay.set('')
            self.C_city.set('')
            self.message_L.config(text=self.message, fg='green')

    def clear(self):
            self.ID.set('')
            self.C_name.set('')
            self.C_street.set('')
            self.C_barangay.set('')
            self.C_city.set('')
            self.C_no.set('')
            self.message_L.config(text=self.message, fg='green')
            self.ID_L.config(image='')

    def print_id(self):
        # Ask the user if they want to print the ID card
        confirm = messagebox.askyesno("Print ID", "Do you want to print the ID card?")

        if confirm:
            try:
                # Set up the printer
                printer_name = win32print.GetDefaultPrinter()
                hprinter = win32print.OpenPrinter(printer_name)
                printer_info = win32print.GetPrinter(hprinter, 2)

                # Create a DC (device context) for the printer
                printer_dc = win32ui.CreateDC()
                printer_dc.CreatePrinterDC(printer_name)

                # Set the orientation to portrait
                printer_dc.StartDoc("ID Card")
                printer_dc.StartPage()
                printer_dc.SetMapMode(win32con.MM_TEXT)

                # Load the ID card image
                id_image = win32ui.CreateBitmap()
                id_image.CreateCompatibleBitmap(printer_dc, 205, 327)  # Adjust the size as needed

                # Select the loaded bitmap
                printer_dc.SelectObject(id_image)

                # Load the image you want to print (modify the path as needed)
                image_path = r'C:\Users\Trisha\PycharmProjects\pythonProject\Library\ID_TUPC-20-0132.png'

                image = I.open(image_path)

                # Draw the image onto the printer DC
                printer_dc.StretchBlt((0, 0, 205, 327), image, (0, 0, image.width, image.height), win32con.SRCCOPY)

                # Clean up and finish printing
                printer_dc.EndPage()
                printer_dc.EndDoc()
                printer_dc.DeleteDC()

                messagebox.showinfo("Printed", "ID card printed successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while printing: {str(e)}")

        else:
            messagebox.showinfo("Print Cancelled", "Printing cancelled by user.")

if __name__ == '__main__':
    root = Tk()
    App = Win(root)
    root.mainloop()
