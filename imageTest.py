
import tkinter as tk
import os

from tkinter import filedialog   #Separate submodule, so requires you to import it explicitly.
from PIL import Image, ImageTk, ImageDraw

class EraserApp:
    def __init__(self, root):
        self.root = root

        # Ask the user to select an image file
        image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if not image_path:
            print("No file selected.")
            root.quit()
            return

        self.image = Image.open(image_path).convert("RGBA")
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(root, width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.pack()
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)


        #zoom
        self.canvas.bind("<MouseWheel>", self.on_zoom)         # Windows / macOS
        self.canvas.bind("<Button-4>", self.on_zoom_linux)     # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_zoom_linux)     # Linux scroll down


        # Store the start point of the rectangle
        self.rect_start = None
        self.rect_id = None

        # Mouse event bindings
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)


        # Button to confirm erasure
        self.erase_button = tk.Button(root, text="Confirm Erase", command=self.confirm_erase)
        self.erase_button.pack()

        # Cancel button
        self.cancel_button = tk.Button(root, text="Cancel Erase", command=self.cancel_selection)
        self.cancel_button.pack(side="left", padx=5)


    def on_press(self, event):
        # Save the starting coordinates when the user presses the mouse
        self.rect_start = (event.x, event.y)
        self.rect_id = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red", width=2)


    def on_drag(self, event):
        # Update the rectangle as the user drags the mouse
        if self.rect_id:
            self.canvas.coords(self.rect_id, self.rect_start[0], self.rect_start[1], event.x, event.y)


    def confirm_erase(self):
        # Get the coordinates of the rectangle
        x1, y1, x2, y2 = self.canvas.coords(self.rect_id)

        # Create a white rectangle over the selected area to "erase"
        draw = ImageDraw.Draw(self.image)
        draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 0))

        # Update the Tkinter image and canvas
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        # Optionally, save the image
        save_path = os.path.join("Image", "erased_image.png")
        self.image.save(save_path)
        self.image.show()  # Opens with default image viewer


    def cancel_selection(self):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None
            self.rect_start = None


# Create and run the application
root = tk.Tk()
app = EraserApp(root)
root.mainloop()

