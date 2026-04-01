"""
Report generator — converts conclusion data into exportable PDF/JSON reports.

Pipeline: conclusion JSON → HTML template → PDF (via WeasyPrint)
"""


def generate_json_report(conclusion: dict, audit_results: list[dict]) -> dict:
    """Generate a structured JSON report."""
    # TODO: implement
    pass


def generate_pdf_report(conclusion: dict, audit_results: list[dict]) -> bytes:
    """Generate a PDF report from conclusion data.

    Uses WeasyPrint: JSON → HTML → PDF
    """
    # TODO: implement with WeasyPrint
    pass
