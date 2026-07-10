import os
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract

class ContractOCRPipeline:
    def __init__(self, tesseract_binary_path: str = None):
        if tesseract_binary_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_binary_path

    def process_pdf(self, pdf_path: str, dpi: int = 200) -> str:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Target PDF file not located at {pdf_path}")
            
        print(f"🔍 Initializing OCR Engine for: {Path(pdf_path).name}")
        try:
            pages = convert_from_path(pdf_path, dpi=dpi)
            extracted_text_blocks = []
            
            for i, page_image in enumerate(pages, start=1):
                print(f"   ⚙️ Processing page layer [{i}/{len(pages)}]...")
                page_text = pytesseract.image_to_string(page_image)
                extracted_text_blocks.append(f"--- START OF PAGE {i} ---\n{page_text}")
                
            return "\n\n".join(extracted_text_blocks)
            
        except Exception as e:
            print(f"❌ Critical pipeline failure executing OCR: {str(e)}")
            raise e

if __name__ == "__main__":
    pipeline = ContractOCRPipeline()
    TEST_FILE = "data/raw_contracts/sample.pdf"
    
    if os.path.exists(TEST_FILE):
        text_output = pipeline.process_pdf(TEST_FILE)
        print("\n📝 Sample Text Extracted:\n", text_output[:300])
    else:
        print(f"ℹ️ Place a test document at '{TEST_FILE}' to verify OCR functionality.")
