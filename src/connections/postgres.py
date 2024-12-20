from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

engine: AsyncEngine


async def get_postgres_session() -> AsyncSession:
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # noqa: F821
    async with async_session() as session:
        yield session
