import tkinter as tk
from PIL import Image, ImageTk
import cv2
import pytesseract

class MatchingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.cap = None

        # Create a canvas that covers the entire frame with a background color
        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg='#5D1C1C')
        self.canvas.pack()

        # Create a label for the text extraction results
        self.text_result_label = tk.Label(self, text='', font=('inter', 14), fg='white', bg='#5D1C1C')
        self.text_result_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Define the background color for the scan button
        scan_button_bg_color = '#5D1C1C'

        # Create Scan button with background color
        self.scan_button = tk.Button(self, text='TAP TO SCAN YOUR COR', font=('caveat brush', 18), fg='white', bg=scan_button_bg_color,
                                     width=28, command=self.capture_and_extract)
        self.scan_button.place(relx=0.5, rely=0.93, anchor=tk.CENTER)

        # Call the function to start the camera preview
        self.open_camera()

    def open_camera(self):
        # Start the camera preview
        self.cap = cv2.VideoCapture(0)
        self.show_camera_preview()

    def show_camera_preview(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)

            # Adjust the dimensions of the image (width, height)
            img = img.resize((800, 500))

            img_tk = ImageTk.PhotoImage(img)
            self.canvas.delete("all")  # Clear previous drawings

            # Calculate the position to center the camera preview
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            img_width = img_tk.width()
            img_height = img_tk.height()

            x = (canvas_width - img_width) // 2
            y = (canvas_height - img_height) // 2

            self.canvas.create_image(x, y, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk
            self.after(10, self.show_camera_preview)

            # Create the sub-heading label at the top center of the camera preview
            sub_heading_label_text = 'Please scan your Certificate of Registration'
            sub_heading_label = self.canvas.create_text(canvas_width // 2, y -100 + 50,
                                                        text=sub_heading_label_text, font=('caveat brush', 20),
                                                        fill='White')

    def close_camera(self):
        # Release the camera object
        if self.cap is not None:
            self.cap.release()

    def on_leave(self):
        # Call the function to close the camera when leaving the page
        self.close_camera()

    def capture_and_extract(self):
        if self.cap is None:
            self.start_camera()

        ret, frame = self.cap.read()
        if ret:
            self.stop_camera()
            extracted_text = self.extract_text_from_image(frame)
            self.text_result_label.config(text=extracted_text)
            print("Extracted Text:", extracted_text)

    def extract_text_from_image(self, image):
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text

if __name__ == "__main__":
    app = tk.Tk()
    matching_page = MatchingPage(app, None)
    matching_page.pack(fill="both", expand=True)
    app.mainloop()

    def show_popup(self):
        # Create a Toplevel window (pop-up)
        popup = tk.Toplevel(self)

        # Set the title and size of the pop-up window
        popup.title("Capture Image")
        popup.geometry("400x200")

        # Add widgets and functionality to the pop-up window
        label = tk.Label(popup, text="This is a pop-up window.")
        label.pack(pady=20)

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack()

        # Create the camera preview label
        self.camera_preview_label = tk.Label(self, width=500, height=80, bg='white')
        self.camera_preview_label.place(relx=0.9, rely=0.3, anchor=tk.E, width=300, height=300)