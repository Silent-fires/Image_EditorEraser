
from PIL import Image, ImageTk, ImageDraw

class zoom_fuction:
    def __init__(self, canvas, image, canvas_image, parent):
        self.canvas = canvas
        self.image = image
        self.canvas_image = canvas_image
        self.parent = parent

        self.drag_start = None

        self.zoom_scale = 1.0 # default
        self.zoom_step = 1.1  # 10% zoom in/out
        self.zoom_scale = min(max(self.zoom_scale, 0.2), 10) # min and max zoom

    def on_zoom(self, event):
        # Get mouse position before zoom
        canvas_mouse_x = self.canvas.canvasx(event.x)
        canvas_mouse_y = self.canvas.canvasy(event.y)

        # Calculate offset from image center
        img_x, img_y = self.canvas.coords(self.canvas_image)
        offset_x = canvas_mouse_x - img_x
        offset_y = canvas_mouse_y - img_y

        if event.delta > 0:
            self.zoom_scale *= self.zoom_step
        else:
            self.zoom_scale /= self.zoom_step
        self.apply_zoom()

        # After zoom, reposition image so the same point stays under the cursor
        # new_img_width = int(self.image.width * self.zoom_scale)
        # new_img_height = int(self.image.height * self.zoom_scale)

        new_img_x = canvas_mouse_x - offset_x * self.zoom_step if event.delta > 0 else canvas_mouse_x - offset_x / self.zoom_step
        new_img_y = canvas_mouse_y - offset_y * self.zoom_step if event.delta > 0 else canvas_mouse_y - offset_y / self.zoom_step

        self.canvas.coords(self.canvas_image, new_img_x, new_img_y)
        self.parent.update_grid()

    def on_zoom_linux(self, event):
        if event.num == 4:
            self.zoom_scale *= self.zoom_step
        elif event.num == 5:
            self.zoom_scale /= self.zoom_step
        self.apply_zoom()

    def apply_zoom(self):
        # Resize image
        zoomed_image = self.image.resize(
            (int(self.image.width * self.zoom_scale), int(self.image.height * self.zoom_scale)),
            Image.LANCZOS
        )
        self.tk_image = ImageTk.PhotoImage(zoomed_image)

        # Update canvas size and image
        self.canvas.itemconfig(self.canvas_image, image=self.tk_image)

    def reset_zoom(self):
        self.zoom_scale = 1.0
        self.apply_zoom()

        self.canvas.coords(self.canvas_image, 0, 0)


    def start_drag(self, event):
        self.drag_start = (event.x, event.y)

    def drag_image(self, event):
        if self.drag_start is not None:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            self.canvas.move(self.canvas_image, dx, dy)
            self.drag_start = (event.x, event.y)
            self.parent.update_grid()