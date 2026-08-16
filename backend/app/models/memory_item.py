import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

# Placeholder dimension — revisit once the Phase 2 embedding model is chosen (e.g. Voyage AI).
EMBEDDING_DIM = 1536


class MemoryItem(Base):
    """A single ingested chunk from any connector (email, doc, message, etc).

    This is a Phase-1 smoke-test model: it exists mainly to prove the pgvector
    extension and vector column type work end-to-end via Alembic migrations.
    The real schema (entities, categories, source-specific metadata) is Phase 2/3 work.
    """

    __tablename__ = "memory_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    item_metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
