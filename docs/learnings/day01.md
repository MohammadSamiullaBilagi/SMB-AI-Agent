# Day 1 — Project Setup + Python Foundations

## What I studied
- Pydantic v2: field_validator, model_validator, BaseModel
- Type hints: Optional, List, dict
- async/await: basic concept (will go deeper on Day 12)

## What I built
- Full project folder structure
- Pydantic models: DocumentChunk and BusinessDocument
- Validation tests — all 4 passing

## Design decision I made
Chose to add a `doc_type` validator that restricts to known types.
Reasoning: if unknown file types get ingested, retrieval quality 
drops silently. Better to fail fast at the model level.

## What confused me
When i wrote test_models.py for validating the chunk id and document type, i got module not found error for backend, so i fixed it by adding __init__.py in backend folder, and added sys.path module so that whenever code is ran, python can find project root when running script directly

## How this connects to interviews
If asked "how do you validate data in your pipeline" — I can 
now explain Pydantic validators with a real example from my project.