OCR Text Capture Tool for Windows

【ソフト名】
TextCapture - OCR文字認識ツール（英語のみ対応）

【概要】
このツールは、画面上の任意の範囲を選択して英語のテキストをOCRで読み取る簡易アプリです。
Tesseract OCRをバックエンドに使用しています。

【必要な環境】
- Python 3.8 以降
- 以下のPythonライブラリ：
  - pytesseract
  - pillow
  - keyboard
  - pyperclip
  - pyautogui

【セットアップ手順】
1. Tesseract OCRをインストールしてください。
   ダウンロード先（公式）：https://github.com/tesseract-ocr/tesseract

2. `tesseract.exe` のパスをスクリプト内の `TESSERACT_PATH` に設定してください。
   例：
   ```python
   TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



本ツールはGoogleのTesseract OCRを利用しています。TesseractはApache License 2.0のもと配布されています。

ユーザーは、Tesseractのライセンスに従ってご利用ください。

本ソフトを利用することによって生じた問題や損害について、開発者は一切の責任を負いかねます。