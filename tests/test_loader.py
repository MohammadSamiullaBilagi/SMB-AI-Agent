import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ingestion.loader import DocumentLoader
from pathlib import Path

loader = DocumentLoader()


def test_csv_loading():
    print("\n--- Testing CSV Loader ---")
    results = loader.load("sample_data/sales.csv")
    print(f"Loaded {len(results)} rows")
    print("First row:")
    print(f"  {results[0]}")
    print("Last row:")
    print(f"  {results[-1]}")
    assert len(results) == 10, f"Expected 10 rows, got {len(results)}"
    assert "Masala Dosa" in results[0]
    assert "Rs." in results[0]
    print("✅ CSV test passed")


def test_txt_loading():
    print("\n--- Testing TXT Loader ---")
    results = loader.load("sample_data/feedback.txt")
    print(f"Loaded {len(results)} paragraphs")
    for i, para in enumerate(results):
        print(f"  Para {i+1}: {para[:60]}...")
    assert len(results) >= 3
    print("✅ TXT test passed")


def test_unsupported_file():
    print("\n--- Testing Unsupported File Type ---")
    try:
        loader.load("sample_data/fake.xlsx")
        print("❌ Should have raised ValueError")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")
    except FileNotFoundError as e:
        print(f"✅ Correctly rejected (file not found): {e}")


def test_file_not_found():
    print("\n--- Testing File Not Found ---")
    try:
        loader.load("sample_data/nonexistent.csv")
        print("❌ Should have raised FileNotFoundError")
    except FileNotFoundError as e:
        print(f"✅ Correctly raised FileNotFoundError: {e}")


if __name__ == "__main__":
    test_csv_loading()
    test_txt_loading()
    test_unsupported_file()
    test_file_not_found()
    print("\n✅ All Day 2 loader tests passed.")