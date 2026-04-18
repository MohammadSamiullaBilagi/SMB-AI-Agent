import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ingestion.chunker import TextChunker
from backend.ingestion.loader import DocumentLoader
loader = DocumentLoader()
chunker = TextChunker(chunk_size=300, overlap=50)


def test_basic_chunking():
    print("\n--- Test 1: Basic Chunking ---")
    # 400 words should produce 2 chunks with 300/50 settings
    text = " ".join(["word"] * 400)
    chunks = chunker.chunk_text(text, source_file="test.txt")
    print(f"400 words → {len(chunks)} chunks")
    for i, c in enumerate(chunks):
        print(f"  Chunk {i}: {c.metadata['word_count']} words, "
              f"id={c.chunk_id}")
    assert len(chunks) == 2, f"Expected 2 chunks, got {len(chunks)}"
    print("✅ Basic chunking passed")


def test_short_text_single_chunk():
    print("\n--- Test 2: Short Text → Single Chunk ---")
    text = "This is a short feedback entry from a customer."
    chunks = chunker.chunk_text(text, source_file="feedback.txt")
    print(f"Short text → {len(chunks)} chunk(s)")
    assert len(chunks) == 1
    print("✅ Short text test passed")


def test_overlap():
    print("\n--- Test 3: Overlap Check ---")
    # 350 words — chunk 0 gets words 0-299, chunk 1 gets 250-349
    words = [f"word{i}" for i in range(350)]
    text = " ".join(words)
    chunks = chunker.chunk_text(text, source_file="overlap_test.txt")
    print(f"350 words → {len(chunks)} chunks")

    chunk0_words = set(chunks[0].content.split())
    chunk1_words = set(chunks[1].content.split())
    overlap_words = chunk0_words & chunk1_words

    print(f"  Overlapping words: {len(overlap_words)}")
    assert len(overlap_words) >= 40, \
        f"Expected ~50 overlapping words, got {len(overlap_words)}"
    print("✅ Overlap test passed")


def test_invalid_overlap():
    print("\n--- Test 4: Invalid Config Rejected ---")
    try:
        bad_chunker = TextChunker(chunk_size=100, overlap=100)
        print("❌ Should have raised ValueError")
    except ValueError as e:
        print(f"✅ Correctly rejected: {e}")


def test_csv_pipeline():
    print("\n--- Test 5: Full CSV → Loader → Chunker Pipeline ---")
    texts = loader.load("sample_data/sales.csv")
    chunks = chunker.chunk_documents(texts, source_file="sales.csv")
    print(f"sales.csv → {len(texts)} rows → {len(chunks)} chunks")
    print(f"First chunk preview:")
    print(f"  ID: {chunks[0].chunk_id}")
    print(f"  Content: {chunks[0].content[:80]}...")
    print(f"  Words: {chunks[0].metadata['word_count']}")
    assert len(chunks) >= 1
    assert "Masala Dosa" in chunks[0].content
    print("✅ CSV pipeline test passed")


def test_feedback_pipeline():
    print("\n--- Test 6: Full TXT → Loader → Chunker Pipeline ---")
    texts = loader.load("sample_data/feedback.txt")
    chunks = chunker.chunk_documents(texts, source_file="feedback.txt")
    print(f"feedback.txt → {len(texts)} paragraphs → {len(chunks)} chunks")
    for c in chunks:
        print(f"  Chunk {c.chunk_index}: {c.metadata['word_count']} words")
    assert len(chunks) >= 1
    print("✅ Feedback pipeline test passed")


if __name__ == "__main__":
    test_basic_chunking()
    test_short_text_single_chunk()
    test_overlap()
    test_invalid_overlap()
    test_csv_pipeline()
    test_feedback_pipeline()
    print("\n✅ All Day 3 chunker tests passed.")