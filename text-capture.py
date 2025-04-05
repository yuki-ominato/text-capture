import tkinter as tk
from PIL import ImageGrab
import pytesseract
import ctypes

# DPIスケーリングを無効化（これが最も重要！）
ctypes.windll.user32.SetProcessDPIAware()

# Tesseractのインストールパス（必要に応じて変更）
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class ScreenOCRApp:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None

        # 透明な全画面ウィンドウ
        self.root = tk.Tk()
        self.root.attributes("-alpha", 0.3)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.root.mainloop()

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_move_press(self, event):
        curX, curY = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        self.root.destroy()

        x1 = int(min(self.start_x, end_x))
        y1 = int(min(self.start_y, end_y))
        x2 = int(max(self.start_x, end_x))
        y2 = int(max(self.start_y, end_y))

        # 正確な座標でキャプチャ
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save("selected_area.png")

        text = pytesseract.image_to_string(img, lang="eng")
        print("===== OCR結果 =====")
        print(text)
        print("===================")

# 実行
ScreenOCRApp()
