import csv
import pdfplumber
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DocumentLoader:
    """
    Loads CSV, PDF, and plain text files.
    Returns a list of raw text strings — one string per logical unit.
    For CSV: one string per row (converted to natural language).
    For PDF: one string per page.
    For TXT: one string for the whole file (split by double newline).
    """

    SUPPORTED_TYPES = {'.csv', '.pdf', '.txt'}

    def load(self, filepath: str | Path) -> list[str]:
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        suffix = filepath.suffix.lower()

        if suffix not in self.SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported file type '{suffix}'. "
                f"Supported: {self.SUPPORTED_TYPES}"
            )

        logger.info(f"Loading {suffix} file: {filepath.name}")

        if suffix == '.csv':
            return self._load_csv(filepath)
        elif suffix == '.pdf':
            return self._load_pdf(filepath)
        elif suffix == '.txt':
            return self._load_txt(filepath)

    def _load_csv(self, filepath: Path) -> list[str]:
        """
        Converts each CSV row into a natural language sentence.
        Example: "On 2024-01-15, sold 45 units of Masala Dosa
                  at Rs.100 each, total Rs.4500, during breakfast."
        This makes semantic search work — embeddings understand
        sentences, not raw key=value pairs.
        """
        rows = []
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = self._row_to_natural_language(row)
                if text:
                    rows.append(text)

        logger.info(f"Loaded {len(rows)} rows from {filepath.name}")
        return rows

    def _row_to_natural_language(self, row: dict) -> Optional[str]:
        """
        Converts a CSV row dict to a readable sentence.
        Handles the sales CSV format specifically.
        Falls back to generic format for unknown columns.
        """
        # Known sales format
        if all(k in row for k in ['date', 'item', 'quantity',
                                   'unit_price', 'total']):
            service = row.get('service', 'unknown')
            return (
                f"On {row['date']}, sold {row['quantity']} units of "
                f"{row['item']} at Rs.{row['unit_price']} each, "
                f"total Rs.{row['total']}, during {service} service."
            )

        # Generic fallback — join all key-value pairs
        parts = [f"{k}: {v}" for k, v in row.items() if v.strip()]
        return ", ".join(parts) if parts else None

    def _load_pdf(self, filepath: Path) -> list[str]:
        """
        Extracts text page by page from a PDF.
        Each page becomes one text block.
        Skips empty pages.
        """
        pages = []
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and text.strip():
                    # Clean up extra whitespace
                    cleaned = " ".join(text.split())
                    pages.append(cleaned)
                else:
                    logger.warning(
                        f"Page {page_num + 1} in {filepath.name} "
                        f"has no extractable text — skipping."
                    )

        logger.info(
            f"Loaded {len(pages)} pages from {filepath.name}"
        )
        return pages

    def _load_txt(self, filepath: Path) -> list[str]:
        """
        Reads plain text files.
        Splits on double newlines (paragraph breaks).
        Filters out empty paragraphs.
        """
        with open(filepath, encoding='utf-8') as f:
            content = f.read()

        # Split by paragraph (double newline)
        paragraphs = [p.strip() for p in content.split('\n\n')]
        paragraphs = [p for p in paragraphs if len(p) > 10]

        logger.info(
            f"Loaded {len(paragraphs)} paragraphs from {filepath.name}"
        )
        return paragraphs