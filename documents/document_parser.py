from paddleocr import PaddleOCR
from loguru import logger

class DocumentProcessingInput:
    def __init__(self, image, message):
        self.image = image
        self.message = message
        
class DocumentParser: 
    def __init__(self, model_name: str) -> None:
        try:
            self.ocr_model = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False)
        except Exception as e:
            logger.error(f"Failed to initialize OCR model: {e}")
        
    @classmethod
    def process_document(self, input: DocumentProcessingInput) -> str:
        result = self.ocr_model.predict(input.image)
        return result
        