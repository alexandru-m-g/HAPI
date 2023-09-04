from typing import List

from datetime import datetime

from sqlalchemy import Boolean, Integer, String, CHAR, Text, DateTime, text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class DBLocation(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    reference_period_start: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )


class DBAdmin1(Base):
    __tablename__ = "admin1"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location_ref: Mapped[int] = mapped_column(ForeignKey("location.id"))
    code: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    is_unspecified: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))
    reference_period_start: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )

    location = relationship("DBLocation")


class DBAdmin2(Base):
    __tablename__ = "admin2"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    admin1_ref: Mapped[int] = mapped_column(ForeignKey("admin1.id"))
    code: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    is_unspecified: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))
    reference_period_start: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )
    admin1 = relationship("DBAdmin1")


class DBSector(Base):
    __tablename__ = "sector"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    reference_period_start: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )


class DBResource(Base):
    __tablename__ = "resource"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_ref: Mapped[int] = mapped_column(ForeignKey("dataset.id"), nullable=True)
    hdx_link: Mapped[str] = mapped_column(String(512), nullable=False)
    code: Mapped[str] = mapped_column(String(128), nullable=False)
    filename: Mapped[str] = mapped_column(String(256), nullable=False)
    format: Mapped[str] = mapped_column(String(32), nullable=False)
    update_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    is_hxl: Mapped[bool] = mapped_column(Boolean, nullable=False, index=True)
    api_link: Mapped[str] = mapped_column(String(1024), nullable=False)

    dataset:Mapped['DBDataset'] = relationship('DBDataset')

class DBDataset(Base):
    __tablename__ = "dataset"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hdx_link: Mapped[str] = mapped_column(String(512), nullable=False)
    code: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(1024), nullable=False)
    provider_code: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    provider_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    api_link: Mapped[str] = mapped_column(String(1024), nullable=False)

    resources: Mapped[List['DBResource']] = relationship("DBResource")


class DBOrg(Base):
    __tablename__ = "org"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hdx_link: Mapped[str] = mapped_column(String(1024), nullable=False)
    acronym: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    org_type_code: Mapped[str] = mapped_column(ForeignKey("org_type.code"))
    reference_period_start: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )

    org_type = relationship("DBOrgType")


class DBOrgType(Base):
    __tablename__ = "org_type"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    description: Mapped[str] = mapped_column(String(512), nullable=False)


class DBGender(Base):
    __tablename__ = "gender"

    code: Mapped[str] = mapped_column(CHAR(1), primary_key=True)
    description: Mapped[str] = mapped_column(String(256))


class DBAgeRange(Base):
    __tablename__ = "age_range"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    age_min: Mapped[int] = mapped_column(Integer, nullable=False)
    age_max: Mapped[int] = mapped_column(Integer, nullable=True)


class OperationalPresence(Base):
    __tablename__ = 'operational_presence'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_ref = mapped_column(
        ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    org_ref = mapped_column(ForeignKey("org.id", onupdate="CASCADE"))
    sector_code = mapped_column(ForeignKey("sector.code", onupdate="CASCADE"))
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE")
    )
    reference_period_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )
    source_data: Mapped[str] = mapped_column(Text, nullable=True)

    resource = relationship("DBResource")
    org = relationship("DBOrg")
    sector = relationship("DBSector", lazy='raise')
    admin2 = relationship("DBAdmin2")

# Index('operational_presence_1_reference_period_start_index', OperationalPresence.reference_period_start) sdfsdf adsfgd sdfg sdfgdsfg
