from io import BytesIO
import fitz
from docx import Document
from pathlib import Path
from myapp.schemas.resume_extraction import ResumeExtractionInput

class DocumentService:

    def __init__(self, file_type):
        self.file_type = file_type
 
    def extract_text(self, file_name: str, content: bytes) -> ResumeExtractionInput:
        extension = file_name.lower().split(".")[-1]

        if extension == "pdf":
            print("Extracting PDF content...")
            return self._extract_pdf(content)

        if extension == "docx":
            return self._extract_docx(content)

        if extension == "txt":
            return self._extract_txt(content)

        raise ValueError("Unsupported file type")

    def _extract_pdf(self, content: bytes) -> ResumeExtractionInput:
        text = []
        links = []

        with fitz.open(stream=content, filetype="pdf") as document:
            for page in document:
                text.append(page.get_text())
                if self.file_type == "resume":
                    links.extend(
                        link["uri"]
                        for link in page.get_links()
                        if link.get("uri")
                    )

        text = "\n".join(text).strip()
        print(text)
        print(links)
        return ResumeExtractionInput(text=text, links=links)

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
        print(text)
        print(links)
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