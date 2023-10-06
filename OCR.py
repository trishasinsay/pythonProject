import tkinter as tk
import cv2
from PIL import Image, ImageTk
import pytesseract
import mysql.connector
from tkinter import messagebox  # Import messagebox module



class MatchingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.cap = None
        self.photo = None
        self.camera_preview_initialized = False

        # Create a canvas to display the camera preview
        self.camera_canvas = tk.Canvas(self, width=640, height=480)
        self.camera_canvas.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Create a StringVar to hold the extracted text
        self.extracted_text_var = tk.StringVar()

        # Call the function to initialize and display the camera preview
        self.initialize_camera_preview()

    def initialize_camera_preview(self):
        if not self.camera_preview_initialized:
            try:
                # Open the camera (replace '0' with the correct camera index or device name)
                self.cap = cv2.VideoCapture(1)
                if not self.cap.isOpened():
                    raise Exception("Camera not found or cannot be opened.")
                self.camera_preview_initialized = True
            except Exception as e:
                print(f"Error initializing camera: {str(e)}")

        self.update_camera_preview()

    def update_camera_preview(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        if ret:
            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Extract text and draw a bounding box
            extracted_text, bbox_image = self.extract_text_from_image(frame_rgb)

            # Update the extracted text using StringVar
            self.extracted_text_var.set(extracted_text)

            # Convert the frame with the bounding box to PhotoImage
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(bbox_image))

            # Update the canvas with the new frame
            self.camera_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            # Check for a match in the database
            self.check_matching(extracted_text)

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

    def check_matching(self, extracted_text):
        # Check if extracted_text is not empty
        if extracted_text:
            # Replace with your database credentials
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="030702",
                database="db_test1"
            )

            cursor = db.cursor()

            # Execute a SQL query to retrieve the ID numbers from the database
            cursor.execute("SELECT id_number FROM tbl_test1")
            results = cursor.fetchall()

            # Close the database connection
            db.close()

            # Extract the ID numbers from the results and normalize them (e.g., remove spaces and convert to uppercase)
            id_numbers = {result[0].strip().upper() for result in results}

            # Normalize the extracted text for comparison
            extracted_text = extracted_text.strip().upper()

            # Debug print statements
            print("Extracted Text:", extracted_text)  # Cleaned and normalized extracted text

            # Check if the normalized extracted text is in the set of normalized ID numbers
            if extracted_text in id_numbers:
                print("Matched")
                # Show a confirmation message
                messagebox.showinfo("Validation Successful", "Your ID is now Validated")
                # Close the matching page
                self.on_leave()
            else:
                print("Not Matched")
        else:
            print("No text detected")

    def stop_camera(self):
        # Release the camera
        if self.cap is not None:
            self.cap.release()

    def on_leave(self):
        # Call the function to close the camera when leaving the page
        self.stop_camera()

# Example usage
if __name__ == "__main__":
    app = tk.Tk()
    matching_page = MatchingPage(app, None)
    matching_page.pack(fill="both", expand=True)
    app.mainloop()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title('TECHNOLOGICAL UNIVERSITY OF THE PHILIPPINES-CAVITE')
        self.controller.state('zoomed')
        self.controller.iconphoto(False, tk.PhotoImage(file='tup logo 1.png'))
