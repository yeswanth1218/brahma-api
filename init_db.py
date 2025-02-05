# init_db.py
import asyncio
from database import engine, Base
from models import UserInput

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init())
