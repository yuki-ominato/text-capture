import tkinter as tk
from PIL import ImageGrab
import pytesseract
import ctypes
import keyboard  # ホットキー用
import threading  # 別スレッドでGUIを起動
import pyperclip  # クリップボードにコピー（標準ではないがよく使われる）

# 追加ライブラリのインストールが必要:
# pip install keyboard pyperclip

# DPIスケーリング無効化（座標のズレ防止）
ctypes.windll.user32.SetProcessDPIAware()

# Tesseractパスを適宜修正
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class ScreenOCRApp:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None

        # フルスクリーンで透明な選択ウィンドウ
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
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

    def on_move_press(self, event):
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        self.root.destroy()

        x1 = int(min(self.start_x, end_x))
        y1 = int(min(self.start_y, end_y))
        x2 = int(max(self.start_x, end_x))
        y2 = int(max(self.start_y, end_y))

        # 指定範囲をキャプチャ
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save("selected_area.png")  # デバッグ用

        # OCRで文字抽出
        text = pytesseract.image_to_string(img, lang="eng")

        # 結果表示 + クリップボードにコピー
        print("===== OCR結果 =====")
        print(text)
        print("===================")
        pyperclip.copy(text)
        print("▶ 結果をクリップボードにコピーしました！")

# OCR処理を別スレッドで実行（GUIがブロックされないように）
def run_ocr():
    threading.Thread(target=ScreenOCRApp).start()

# ホットキー登録（Ctrl + Shift + O）
keyboard.add_hotkey('ctrl+shift+o', run_ocr)

print("🔍 Ctrl + Shift + O を押すとOCRモードが起動します")
print("❌ Ctrl + C で終了")

keyboard.wait()  # 永久に待機

# text = pytesseract.image_to_string(img, lang="eng")

