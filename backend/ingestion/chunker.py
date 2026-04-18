import uuid
from pathlib import Path
from backend.ingestion.models import DocumentChunk
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """
    Splits raw text into overlapping word-level chunks.
    Each chunk becomes a DocumentChunk with a unique ID.

    Design decisions:
    - Word-level splitting (not character or sentence level)
      because CSV rows don't have clean sentence boundaries.
    - Overlap of 50 words prevents concepts from being cut
      at chunk boundaries.
    - chunk_size=300 words fits ~5-10 sales rows per chunk,
      giving the LLM enough context without noise.
    """

    def __init__(self, chunk_size: int = 300, overlap: int = 50):
        if overlap >= chunk_size:
            raise ValueError(
                f"Overlap ({overlap}) must be less than "
                f"chunk_size ({chunk_size})"
            )
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(
        self,
        text: str,
        source_file: str,
        chunk_index_offset: int = 0
    ) -> list[DocumentChunk]:
        """
        Chunks a single text string into DocumentChunk objects.

        Args:
            text: The raw text to chunk.
            source_file: Filename this text came from (for metadata).
            chunk_index_offset: Start index if chunking multiple texts
                                from the same file.

        Returns:
            List of DocumentChunk objects.
        """
        words = text.split()

        if not words:
            logger.warning(f"Empty text from {source_file}, skipping.")
            return []

        # If the text is shorter than one chunk, return it as-is
        if len(words) <= self.chunk_size:
            chunk = self._make_chunk(
                words=words,
                source_file=source_file,
                chunk_index=chunk_index_offset
            )
            return [chunk] if chunk else []

        chunks = []
        start = 0
        idx = chunk_index_offset

        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk = self._make_chunk(
                words=words[start:end],
                source_file=source_file,
                chunk_index=idx
            )
            if chunk:
                chunks.append(chunk)
                idx += 1

            # If we've reached the end, stop
            if end == len(words):
                break

            # Move forward by (chunk_size - overlap)
            start += self.chunk_size - self.overlap

        return chunks

    def chunk_documents(
        self,
        texts: list[str],
        source_file: str
    ) -> list[DocumentChunk]:
        """
        Chunks a list of texts (e.g. all rows from one CSV file).
        Maintains a global chunk index across all texts.

        This is the main method you'll call from the pipeline.
        """
        all_chunks = []
        global_index = 0

        for text in texts:
            chunks = self.chunk_text(
                text=text,
                source_file=source_file,
                chunk_index_offset=global_index
            )
            all_chunks.extend(chunks)
            global_index += len(chunks)

        logger.info(
            f"Created {len(all_chunks)} chunks from "
            f"{len(texts)} texts in {source_file}"
        )
        return all_chunks

    def _make_chunk(
        self,
        words: list[str],
        source_file: str,
        chunk_index: int
    ) -> DocumentChunk | None:
        """
        Creates a single DocumentChunk from a list of words.
        Returns None if the content is too short (filtered by Pydantic).
        """
        content = " ".join(words)

        try:
            return DocumentChunk(
                chunk_id=f"{Path(source_file).stem}_{chunk_index}",
                content=content,
                source_file=source_file,
                chunk_index=chunk_index,
                metadata={
                    "word_count": len(words),
                    "source_file": source_file,
                }
            )
        except Exception as e:
            logger.warning(f"Skipping chunk {chunk_index}: {e}")
            return None