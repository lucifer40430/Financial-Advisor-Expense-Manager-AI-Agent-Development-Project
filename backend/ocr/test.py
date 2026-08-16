from pathlib import Path

from vision_ocr import vision_transcribe


image_path = Path(r"C:\Users\rajes\OneDrive\Desktop\finacial advisor rag model\backend\ocr\payment.png")

try:

    text = vision_transcribe(image_path)

    print("\n========== OCR RESULT ==========\n")
    print(text)
    print("\n================================\n")

except Exception as e:

    print("OCR Error:", e)