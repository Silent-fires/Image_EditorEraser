
import tkinter as tk
import os

from tkinter import filedialog   #Separate submodule, so requires you to import it explicitly.
from PIL import Image, ImageTk, ImageDraw
from Zoom import zoom_fuction as zf
from Menu import Resizer

class EraserApp:
    def __init__(self, root):
        self.root = root
        self.grid_lines = []
        self.grid_visible = False

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

        # Main container frame                                                        ------------setup areas
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        # Sidebar wrapper frame (holds sidebar + separator)    ---menu
        menu_frame = tk.Frame(main_frame)
        menu_frame.pack(side="left", fill="y")

        # Sidebar on the left                                  ---menu
        sidebar = tk.Frame(menu_frame, width=150, bg="#f0f0f0")
        sidebar.pack(side="left", fill="y")

        # Canvas on the right (inside main_frame)              ---canvas
        self.canvas = tk.Canvas(main_frame, width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        # Create Menu resizer handler                          ---menu
        self.resize = Resizer(sidebar, self.canvas)

        # Black line separator with visible width              ---menu
        separator = tk.Frame(menu_frame, width=5, bg="black", cursor="sb_h_double_arrow")
        separator.pack(side="left", fill="y")
        separator.bind("<ButtonPress-1>", self.resize.start_resize)
        separator.bind("<B1-Motion>", self.resize.perform_resize)
        

        # Create zoom-in handler                                                         ------------zoom-in implement 
        self.zf_h = zf(self.canvas, self.image, self.canvas_image, self)
        #zoom
        self.canvas.bind("<MouseWheel>", self.zf_h.on_zoom)         # Windows / macOS
        self.canvas.bind("<Button-4>", self.zf_h.on_zoom_linux)     # Linux scroll up
        self.canvas.bind("<Button-5>", self.zf_h.on_zoom_linux)     # Linux scroll down
        #moving
        self.canvas.bind("<ButtonPress-3>", self.zf_h.start_drag)  # Right mouse press
        self.canvas.bind("<B3-Motion>", self.zf_h.drag_image)      # Right mouse drag

        #

        # Store the start point of the rectangle                                           ------------shape variables
        self.rect_start = None
        self.rect_id = None

        # Mouse event bindings                                                             ------------mouse control
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)


        # Button to confirm erasure                                                        ------------buttons
        tk.Button(root, text="Confirm Erase", command=self.confirm_erase).pack()
        # Cancel button
        tk.Button(root, text="Cancel Erase", command=self.cancel_selection).pack(side="left", padx=5)
        # Reset Zoom button
        tk.Button(root, text="Reset Zoom", command=self.zf_h.reset_zoom).pack(side="right", padx=5)
        # grid toggle button
        tk.Button(root, text="Toggle Grid", command=self.toggle_grid).pack(side="left", padx=5)


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


    def toggle_grid(self):
        self.grid_visible = not self.grid_visible
        self.update_grid()

    def update_grid(self, spacing=20):
        # Clear previous grid
        for line in self.grid_lines:
            self.canvas.delete(line)
        self.grid_lines = []

        if not self.grid_visible:
            return

        # Calculate grid in image space, scaled by zoom
        zoom = self.zf_h.zoom_scale
        img_w, img_h = self.image.size
        offset_x, offset_y = self.canvas.coords(self.canvas_image)

        for x in range(0, img_w, spacing):
            sx = offset_x + x * zoom
            line = self.canvas.create_line(sx, offset_y, sx, offset_y + img_h * zoom, fill="gray80", dash=(2, 4))
            self.grid_lines.append(line)

        for y in range(0, img_h, spacing):
            sy = offset_y + y * zoom
            line = self.canvas.create_line(offset_x, sy, offset_x + img_w * zoom, sy, fill="gray80", dash=(2, 4))
            self.grid_lines.append(line)


# Create and run the application
root = tk.Tk()
app = EraserApp(root)
root.mainloop()

