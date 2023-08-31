import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from db_models import meta, OperationalPresence, operational_presence

# meta = MetaData()
# t1 = Table("t1", meta, Column("name", String(50), primary_key=True))

op1 = OperationalPresence(sector_code='test_sector', source_data='some data')


async def async_main() -> None:
    engine = create_async_engine(
        "postgresql+asyncpg://hapi:hapi@localhost:45432/hapi",
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

        await conn.execute(
            operational_presence.insert(), [dict(op1)]
        )

    async with engine.connect() as conn:
        # select a Result, which will be delivered with buffered
        # results
        result = await conn.execute(select(operational_presence).where(operational_presence.c.sector_code == "test_sector"))

        print(result.fetchall())

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


asyncio.run(async_main())
