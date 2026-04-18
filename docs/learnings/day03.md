# Day 3 — Text Chunker

## What I studied
- Chunking strategies: fixed-size, semantic, recursive
- Why chunk overlap prevents concept splitting at boundaries
- Word-level vs character-level vs sentence-level splitting

## What I built
- TextChunker class with configurable chunk_size and overlap
- chunk_text() for a single string
- chunk_documents() for a list of strings (full file)
- 6 tests — all passing

## Design decision I made
Used chunk_size=300 words with overlap=50. For sales CSV rows
(~19 words each), this groups ~15 rows per chunk — enough
context for the LLM to spot patterns without noise.
Short texts (< 300 words) return as a single chunk without
padding, which is more natural than forcing them into the window.

## What I want to explore later
Sentence-level chunking using spaCy — would split on actual
sentence boundaries instead of word count. Could improve quality
for longer feedback text. Worth trying in Week 3 polish.

## How this connects to interviews
If asked "what chunk size did you use and why" — I can give a
real answer: 300 words, because my CSV rows are ~19 words each,
so each chunk captures ~15 rows. Overlap at 50 words prevents
boundary splits. Tested both and verified overlap in test 3.