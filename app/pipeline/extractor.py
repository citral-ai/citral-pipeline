"""
Text extraction — extracts text and tables from PDF pages using Docling.

Preserves table structure as markdown for audit accuracy.
"""


async def extract_text_for_node(pdf_path: str, start_page: int, end_page: int) -> str:
    """Extract text from a range of pages, preserving table structure."""
    # TODO: integrate Docling
    # from docling.document_converter import DocumentConverter
    # converter = DocumentConverter()
    # result = converter.convert(pdf_path)
    # return result.document.export_to_markdown()
    pass
