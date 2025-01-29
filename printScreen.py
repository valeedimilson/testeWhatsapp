import tkinter as tk
from PIL import ImageGrab

def on_drag(event):
    global x1, y1, x2, y2
    x2, y2 = event.x, event.y
    canvas.coords(rect, x1, y1, x2, y2)

def on_click(event):
    global x1, y1, x2, y2
    x1, y1 = event.x, event.y
    x2, y2 = x1, y1
    canvas.coords(rect, x1, y1, x2, y2)

def on_release(event):
    global x1, y1, x2, y2
    x2, y2 = event.x, event.y
    
    # Ensure that x1, x2, y1, y2 are in the correct order
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    
    root.withdraw()
    root.update_idletasks()
    screenshot = ImageGrab.grab(bbox=(root.winfo_rootx() + left, root.winfo_rooty() + top, root.winfo_rootx() + right, root.winfo_rooty() + bottom))
    screenshot.save("captura.png")
    
    print("Captura salva como captura.png")
    root.quit()
    root.destroy()

def close(event):
    root.quit()
    root.destroy()


def capture_region():
    global root, canvas, rect

    # if root:
    #     if root.winfo_exists():
    #         print("Fechando a janela Tkinter...")
    #         root.quit()  # Encerra o mainloop
    #         root.destroy()  # Destroi a janela
    
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill=tk.BOTH, expand=True)
    rect = canvas.create_rectangle(0, 0, 0, 0, outline="red", width=2)
    canvas.bind("<ButtonPress-1>", on_click)
    canvas.bind("<ButtonPress-2>", close)
    canvas.bind("<ButtonPress-3>", close)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    root.mainloop()

if __name__ == "__main__":
    capture_region()
