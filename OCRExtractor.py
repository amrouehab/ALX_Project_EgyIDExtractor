import pytesseract
from PIL import Image
from IDModel import IDSample

class OCREngine:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def extract_arabic_text(self, image):
        text = pytesseract.image_to_string(image, lang='ara-Amiri')    
        return text
    def extract_arabic_textFromImagPath(self, image_path):
        # Load the image
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='ara-Amiri')    
        return text
    def extract_numbers(self,image):
        # Perform OCR on the image
        numbers = pytesseract.image_to_string(image, lang='ara_number', config='--psm 6 outputbase digits')  
        return numbers
    def extract_numbersFromImagePath(self,image_path):
        # Load the image
        image = Image.open(image_path)    
        # Perform OCR on the image
        numbers = pytesseract.image_to_string(image, lang='ara_number', config='--psm 6 outputbase digits')  
        return numbers