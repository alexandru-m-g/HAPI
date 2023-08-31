from typing import Optional

from sqlalchemy import Integer, String, Text, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class OperationalPresence1(Base):
    __tablename__ = 'operational_presence_1'

    id = mapped_column(Integer, primary_key=True)
    resource_ref: Mapped[int] = mapped_column(Integer, nullable=False)
    org_ref: Mapped[int] = mapped_column(Integer, nullable=False)
    sector_code: Mapped[str] = mapped_column(String(32), nullable=False)
    admin2_ref: Mapped[int] = mapped_column(Integer, nullable=False)
    source_data: Mapped[str] = mapped_column(Text, nullable=True)

# Index('operational_presence_1_reference_period_start_index', OperationalPresence.reference_period_start)
