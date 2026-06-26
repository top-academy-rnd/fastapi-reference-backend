from sqlalchemy.ext.asyncio import AsyncSession

from models import engine


async def get_session():
    conn = await engine.connect()
    session = AsyncSession(conn, expire_on_commit=False)

    try:
        yield session
    finally:
        await session.close()
        await conn.close()
