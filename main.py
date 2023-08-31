
import uvicorn
from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from orm_models import OperationalPresence1
from pydantic_orm_model import OperationalPresencePydantic
from run_orm_models import get_db, init_db, populate_db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.on_event("startup")
async def startup():
    await init_db()
    await populate_db()


@app.get("/api/themes/3W", response_model=List[OperationalPresencePydantic])
async def get_operational_presences(db: AsyncSession = Depends(get_db), org_ref: int = None):
    '''
    This is the most important endpoint
    '''
    query = select(OperationalPresence1)
    if (org_ref):
        query = query.where(OperationalPresence1.org_ref == org_ref)
    result = await db.execute(
        query
    )
    operational_presences = result.scalars().all()
    return operational_presences

if __name__ == "__main__":
    uvicorn.run(app, port=8844)
