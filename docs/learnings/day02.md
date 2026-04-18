# Day 2 — Document Loader

## What I studied
- pdfplumber: page iteration, extract_text()
- csv.DictReader: reading rows as dictionaries
- pathlib.Path: .exists(), .suffix, clean file handling

## What I built
- DocumentLoader class with CSV, PDF, TXT support
- _row_to_natural_language() — converts raw CSV rows to sentences
- 4 tests — all passing

## Design decision I made
Converted CSV rows to natural language sentences instead of keeping
them as key=value pairs. Reasoning: embedding models understand
sentences, not "quantity=45, item=Masala Dosa". Converting to
natural language improves semantic search quality significantly.

## What confused me
[your own note here]

## How this connects to interviews
If asked "how do you handle different document types in a RAG
pipeline" — I can explain loader abstraction, format-specific
parsing, and why natural language conversion matters for embeddings.