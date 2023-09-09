import tkinter as tk
import cv2
from PIL import Image, ImageTk
import pytesseract
import numpy as np

class MatchingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.cap = None
        self.photo = None
        self.camera_preview_initialized = False

        # Create a canvas to display the camera preview
        self.camera_canvas = tk.Canvas(self, width=640, height=480)
        self.camera_canvas.pack()

        # Create a label for the text extraction results
        self.text_result_label = tk.Label(self, text='', font=('inter', 14), fg='white', bg='#5D1C1C')
        self.text_result_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Define the background color for the scan button
        scan_button_bg_color = '#5D1C1C'

        # Create Scan button with background color
        self.scan_button = tk.Button(self, text='TAP TO SCAN YOUR COR', font=('caveat brush', 18), fg='white', bg=scan_button_bg_color,
                                     width=28, command=self.capture_and_extract)
        self.scan_button.place(relx=0.5, rely=0.96, anchor=tk.CENTER)

        # Call the function to initialize and display the camera preview
        self.initialize_camera_preview()

    def initialize_camera_preview(self):
        if not self.camera_preview_initialized:
            # Open the camera (replace '0' with the correct camera index or device name)
            self.cap = cv2.VideoCapture(1)
            self.camera_preview_initialized = True

        self.update_camera_preview()

    def update_camera_preview(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        if ret:
            # Enhance the color (contrast stretching)
            frame = self.enhance_color(frame)

            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Extract text and draw a bounding box
            extracted_text, bbox_image = self.extract_text_from_image(frame_rgb)
            self.text_result_label.config(text=extracted_text)

            # Convert the frame with the bounding box to PhotoImage
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(bbox_image))

            # Update the canvas with the new frame
            self.camera_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Schedule the update method to be called again after 10ms
        self.after(10, self.update_camera_preview)

    def capture_and_extract(self):
        if not self.camera_preview_initialized:
            self.initialize_camera_preview()

        ret, frame = self.cap.read()
        if ret:
            extracted_text, _ = self.extract_text_from_image(frame)
            self.text_result_label.config(text=extracted_text)
            print("Extracted Text:", extracted_text)

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
            x1, y1, x2, y2 = int(x1 * scale_factor), int(y1 * scale_factor), int(x2 * scale_factor), int(y2 * scale_factor)
            image_rgb = cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 0, 255), 2)

        return extracted_text, image_rgb

    def stop_camera(self):
        # Release the camera
        if self.cap is not None:
            self.cap.release()

    def on_leave(self):
        # Call the function to close the camera when leaving the page
        self.stop_camera()

    def enhance_color(self, frame):
        # Apply contrast stretching or color enhancement here
        # Example: Increase the contrast
        min_value = np.min(frame)
        max_value = np.max(frame)
        frame = ((frame - min_value) / (max_value - min_value) * 255).astype(np.uint8)
        return frame

# Example usage
if __name__ == "__main__":
    app = tk.Tk()
    matching_page = MatchingPage(app, None)
    matching_page.pack(fill="both", expand=True)
    app.mainloop()
