import asyncio
from fastapi import FastAPI
from app.db.session_async import SessionLocalAsync
from app.db.init_db import init_db

app = FastAPI()
async def init() -> None:
    async with SessionLocalAsync() as db:
        await init_db(db)

async def main() -> None:
    # logger.info("Creating initial data")
    await init()
    # logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())