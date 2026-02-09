import fitz 
import pytesseract
from PIL import Image
import pdf2image
import os
import io 
from typing import List, Dict

class OCRProcessor:
    def __init__(self):
        pass
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF or image using OCR"""
        
        if file_path.lower().endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        else:
            return self._extract_from_image(file_path)
    
    def _extract_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using PyMuPDF and Tesseract"""
        text_content = []
        
        try:
            # Try direct text extraction first
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if text.strip():
                    text_content.append(text)
                else:
                    # Fallback to OCR for scanned PDFs
                    text_content.append(self._ocr_page(page))
            doc.close()
        except Exception as e:
            print(f"PDF extraction failed, using OCR: {e}")
            text_content = self._extract_with_pdf2image(pdf_path)
        
        return "\n".join(text_content)
    
    def _extract_from_image(self, image_path: str) -> str:
        """Extract text from image using Tesseract"""
        try:
            return pytesseract.image_to_string(Image.open(image_path))
        except Exception as e:
            print(f"Image OCR failed: {e}")
            return ""
    
    def _ocr_page(self, page) -> str:
        """OCR a single page"""
        pix = page.get_pixmap()
        img_data = pix.tobytes("ppm")
        return pytesseract.image_to_string(Image.open(io.BytesIO(img_data))) 
    
    def _extract_with_pdf2image(self, pdf_path: str) -> List[str]:
        """Extract text using pdf2image and Tesseract"""
        text_content = []
        images = pdf2image.convert_from_path(pdf_path)
        
        for image in images:
            text = pytesseract.image_to_string(image)
            text_content.append(text)
        
        return text_content