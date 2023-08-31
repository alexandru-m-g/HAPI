import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from orm_models import Base, OperationalPresence1


# Create an AsyncEngine
engine = create_async_engine("postgresql+asyncpg://hapi:hapi@localhost:45432/hapi", echo=True)

# Create a custom Session class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True
)

async def get_db() -> AsyncSession:
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def populate_db():
    # Create and use a session
    async with AsyncSessionLocal() as session:  # Automatically begin a new Transaction
        async with session.begin():  # Actually start the Transaction
            op1 = OperationalPresence1(
                resource_ref=1,
                org_ref=2,
                sector_code="Health",
                admin2_ref=3,
                # reference_period_start=datetime.now(),
                # source_data="Sample data"
            )
            op2 = OperationalPresence1(
                resource_ref=1,
                org_ref=3,
                sector_code="Water",
                admin2_ref=4,
                # reference_period_start=datetime.now(),
                source_data="Sample data"
            )
            session.add_all([op1, op2])

        await session.commit()

async def run():
    await init_db()
    await populate_db()

if __name__ == "__main__":
    # Run the async function
    asyncio.run(run())
