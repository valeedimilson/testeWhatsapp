import tkinter as tk
from PIL import ImageGrab

class ScreenCaptureApp:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.rect = None
        self.x1 = self.y1 = self.x2 = self.y2 = 0

    def on_drag(self, event):
        self.x2, self.y2 = event.x, event.y
        self.canvas.coords(self.rect, self.x1, self.y1, self.x2, self.y2)

    def on_click(self, event):
        self.x1, self.y1 = event.x, event.y
        self.x2, self.y2 = self.x1, self.y1
        self.canvas.coords(self.rect, self.x1, self.y1, self.x2, self.y2)

    def on_release(self, event):
        self.x2, self.y2 = event.x, event.y
        left = min(self.x1, self.x2)
        top = min(self.y1, self.y2)
        right = max(self.x1, self.x2)
        bottom = max(self.y1, self.y2)

        self.root.withdraw()
        self.root.update_idletasks()
        screenshot = ImageGrab.grab(bbox=(self.root.winfo_rootx() + left, self.root.winfo_rooty() + top,
                                          self.root.winfo_rootx() + right, self.root.winfo_rooty() + bottom))
        screenshot.save("captura.png")

        print("Captura salva como captura.png")
        self.cleanup()

    def printScreenStopEvent(self, event):
        self.cleanup()

    def cleanup(self):
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None

    def capture_region(self):
        if self.root is not None:
            # If root already exists, prevent creating a new instance
            return

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)

        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect = self.canvas.create_rectangle(0, 0, 0, 0, outline="red", width=2)
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<ButtonPress-2>", self.printScreenStopEvent)
        self.canvas.bind("<ButtonPress-3>", self.printScreenStopEvent)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.root.mainloop()


if __name__ == "__main__":
    capture_app = ScreenCaptureApp()
    capture_app.capture_region()
