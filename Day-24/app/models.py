"""SQLAlchemy database models"""
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Index, DateTime, Text


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    pass


class OperationalLog(Base):
    """Audit log for all operations"""
    __tablename__ = "operational_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reference_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    payload_summary: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    task_id: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    response_data: Mapped[str] = mapped_column(Text, nullable=True)

    # Database query optimization using explicit performance index
    __table_args__ = (
        Index("idx_reference_id", "reference_id"),
        Index("idx_status_created", "status", "created_at"),
    )

    def __repr__(self):
        return f"<OperationalLog(id={self.id}, reference_id='{self.reference_id}', status='{self.status}')>"
