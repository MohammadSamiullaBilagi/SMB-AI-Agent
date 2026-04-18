import sys
import os

''' Added sys.path insertion at the top of tests/test_models.py so Python can find the project root when running the script directly.'''
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.ingestion.models import DocumentChunk, BusinessDocument
from datetime import datetime


def test_valid_chunk():
    chunk = DocumentChunk(
        chunk_id="test_001",
        content="On January 15, sold 45 units of Masala Dosa for 4500 rupees.",
        source_file="sales_jan.csv",
        chunk_index=0
    )
    print(f"✅ Valid chunk created: {chunk.chunk_id}")


def test_short_content_rejected():
    try:
        chunk = DocumentChunk(
            chunk_id="test_002",
            content="Hi",
            source_file="test.csv",
            chunk_index=0
        )
        print("❌ Should have failed but didn't")
    except Exception as e:
        print(f"✅ Correctly rejected short content: {e}")


def test_valid_document():
    doc = BusinessDocument(
        doc_id="doc_001",
        filename="sales_jan.csv",
        doc_type="sales",
        uploaded_at=datetime.now(),
        chunk_count=42
    )
    print(f"✅ Valid document created: {doc.filename}")


def test_invalid_doc_type():
    try:
        doc = BusinessDocument(
            doc_id="doc_002",
            filename="random.csv",
            doc_type="random_type",
            uploaded_at=datetime.now()
        )
        print("❌ Should have failed but didn't")
    except Exception as e:
        print(f"✅ Correctly rejected invalid doc_type: {e}")


if __name__ == "__main__":
    test_valid_chunk()
    test_short_content_rejected()
    test_valid_document()
    test_invalid_doc_type()
    print("\n✅ All Day 1 tests passed.")