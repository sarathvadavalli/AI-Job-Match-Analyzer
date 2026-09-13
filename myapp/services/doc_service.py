from io import BytesIO
import fitz
from docx import Document
from pathlib import Path
import pytesseract
from PIL import Image

from myapp.schemas.resume_extraction import ResumeExtractionInput

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

class DocumentService:

    def __init__(self, file_type):
        self.file_type = file_type
 
    def extract_text(self, file_name: str, content: bytes) -> ResumeExtractionInput:
        extension = file_name.lower().split(".")[-1]

        if extension == "pdf":
            print("Extracting PDF content...")
            text = self._extract_pdf(content)

            if not text:
                text = self._extract_pdf_ocr(content)
            
            return ResumeExtractionInput(text=text, links=[])

        if extension == "docx":
            return self._extract_docx(content)

        if extension == "txt":
            return self._extract_txt(content)

        raise ValueError("Unsupported file type")

    def _extract_pdf(self, content: bytes) -> str:
        text = []

        with fitz.open(stream=content, filetype="pdf") as document:
            for page in document:
                page_text = page.get_text()

                links = "\n".join(
                    link["uri"]
                    for link in page.get_links()
                    if "uri" in link
                )

                text.append(page_text + "\n" + links)

        return "\n".join(text).strip()

    def _extract_pdf_ocr(self, content: bytes) -> str:
        text = []

        with fitz.open(stream=content, filetype="pdf") as document:
            for page in document:

                # Render PDF page as an image
                pixmap = page.get_pixmap(dpi=300)

                # Convert pixmap to bytes
                image_bytes = pixmap.tobytes("png")

                # Convert bytes to PIL Image
                image = Image.open(BytesIO(image_bytes))

                # Run OCR
                page_text = pytesseract.image_to_string(image)

                if page_text.strip():
                    text.append(page_text.strip())

        return "\n".join(text).strip()

    def _extract_docx(self, content: bytes) -> ResumeExtractionInput:
        document = Document(BytesIO(content))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        links = []
        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)
                
            if self.file_type == "resume":
                for hyperlink in paragraph._p.xpath(".//w:hyperlink"):
                    rel_id = hyperlink.get(
                        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
                    )

                    if rel_id:
                        relationship = paragraph.part.rels.get(rel_id)

                        if relationship and relationship.target_ref:
                            links.append(relationship.target_ref)

        text = "\n".join(paragraphs).strip()
        links = list(dict.fromkeys(links))
        return ResumeExtractionInput(text=text, links=links)

    def _extract_txt(self, content: bytes) -> ResumeExtractionInput:
        return ResumeExtractionInput(text=content.decode("utf-8").strip(), links=[])


# try:
#     file_path = Path("D:/AI Projects/JD Extractor/Sample docs/LL.pptx")
#     if not file_path.exists():
#         raise FileNotFoundError(f"File not found: {file_path}")

#     content = file_path.read_bytes()

#     text = DocumentService.extract_text(
#         file_name=file_path.name,
#         content=content
#     )
#     return text
# except Exception as e:
#     return f"Error: {str(e)}"
