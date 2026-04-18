from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class DocumentChunk(BaseModel):
    chunk_id: str
    content: str
    source_file: str
    chunk_index: int
    metadata: dict = {}

    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Chunk content is too short (min 10 chars)')
        return v

    @field_validator('chunk_id')
    @classmethod
    def chunk_id_not_empty(cls, v):
        if not v.strip():
            raise ValueError('chunk_id cannot be empty')
        return v


class BusinessDocument(BaseModel):
    doc_id: str
    filename: str
    doc_type: str  # 'sales', 'feedback', 'invoice', 'other'
    uploaded_at: datetime
    chunk_count: int = 0

    @field_validator('doc_type')
    @classmethod
    def valid_doc_type(cls, v):
        allowed = {'sales', 'feedback', 'invoice', 'other'}
        if v not in allowed:
            raise ValueError(f'doc_type must be one of {allowed}')
        return v