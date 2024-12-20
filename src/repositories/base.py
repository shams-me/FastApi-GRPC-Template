import typing
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
OrderSchemaType = TypeVar("OrderSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, OrderSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.session = session

    async def get(self, model_id: int | UUID) -> Optional[ModelType]:
        stmts = select(self.model).where(self.model.id == model_id)
        return await self.session.scalar(stmts)

    async def get_multi(self, *, page: int = 0, page_size: int = 100) -> tuple[int, list[ModelType]]:
        stmts = select(self.model).offset(page * page_size).limit(page_size)
        return (await self.session.scalars(stmts)).all()

    async def create(self, obj: typing.Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_in_data = jsonable_encoder(obj)
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, *, obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(obj, field, update_data[field])
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def remove(self, *, model_id: int) -> Optional[ModelType]:
        obj = await self.get(model_id=model_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
        return