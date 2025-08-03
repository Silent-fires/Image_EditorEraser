
from PIL import Image, ImageTk, ImageDraw

class zoom_fuction:
    def __init__(self, root):
        self.zoom_scale = 1.0 # default
        self.zoom_step = 1.1  # 10% zoom in/out
        self.zoom_scale = min(max(self.zoom_scale, 0.2), 10) # min and max zoom

    def on_zoom(self, event):
        if event.delta > 0:
            self.zoom_scale *= self.zoom_step
        else:
            self.zoom_scale /= self.zoom_step
        self.apply_zoom()

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
        self.canvas.config(width=zoomed_image.width, height=zoomed_image.height)
        self.canvas.itemconfig(self.canvas_image, image=self.tk_image)