import PyPDF2

class PDFLoader:
    @staticmethod
    def load(uploaded_file) -> list:
        """
        Loads an uploaded PDF file and returns a list of pages with text and metadata.
        Each page is represented as a dictionary:
        {
            "text": str,
            "page_number": int,
            "filename": str
        }
        """
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            pages = []
            filename = getattr(uploaded_file, "name", "unknown_document.pdf")
            
            for idx, page in enumerate(pdf_reader.pages):
                text = page.extract_text() or ""
                pages.append({
                    "text": text,
                    "page_number": idx + 1,
                    "filename": filename
                })
            
            if not pages:
                raise ValueError("The PDF document contains no pages.")
                
            return pages
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF document: {str(e)}")
