import uvicorn
from typing import List, Annotated
from fastapi import FastAPI, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from orm_models import OperationalPresence, DBDataset
from pydantic_orm_model import OperationalPresencePydantic, HTTP409Message
from run_orm_models import get_db, init_db, populate_db

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get(
    '/dataset_delete/{id}',
    responses={status.HTTP_409_CONFLICT: {'description': 'Db integrity err', 'model': HTTP409Message}},
)
async def delete_dataset(id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(DBDataset).options(selectinload(DBDataset.resources)).where(DBDataset.id == id)
        result = await db.execute(query)
        dataset1 = result.scalar_one()
        await db.delete(dataset1)
        await db.commit()
        return {'message': 'Deleted'}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Deletion of dataset would cause a db integrity error'
        )


@app.on_event('startup')
async def startup():
    await init_db()
    await populate_db()
    pass


@app.get('/api/themes/3W', response_model=List[OperationalPresencePydantic])
async def get_operational_presences(
    db: AsyncSession = Depends(get_db),
    org_ref: Annotated[int, Query(gt=0)] = None,
    sector_code: Annotated[str, Query(max_length=10)] = None,
):
    """
    This is the most important endpoint
    """
    query = select(OperationalPresence).options(selectinload(OperationalPresence.sector))
    if org_ref:
        query = query.where(OperationalPresence.org_ref == org_ref)
    if sector_code:
        query = query.where(OperationalPresence.sector_code == sector_code)

    result = await db.execute(query)
    operational_presences = result.scalars().all()
    return operational_presences


if __name__ == '__main__':
    uvicorn.run(app, port=8844)
