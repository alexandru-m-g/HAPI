from sqlalchemy import Column, MetaData
from sqlalchemy import String, Integer, Text
from sqlalchemy import Table

from pydantic import BaseModel

meta = MetaData()
t1 = Table("t1", meta, Column("name", String(50), primary_key=True))

operational_presence = Table(
    'operational_persence', meta,
    Column('id', Integer, primary_key=True),
    Column('sector_code', String(32), nullable=False),
    Column('source_data', Text),
)


class OperationalPresence(BaseModel):
    # id: int = Field(omit_default=True)
    sector_code: str
    source_data: str
