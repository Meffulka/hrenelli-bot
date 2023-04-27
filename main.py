import aioschedule as schedule
import asyncio
from alembic import command
from alembic.config import Config
from bot import client
import config
import jobs

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

async def scheduler():
    schedule.every(5).minutes.do(jobs.update_user)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

async def main():
    run_migrations()
    asyncio.create_task(client.start(config.DC_TOKEN))
    await scheduler()

if __name__ == "__main__":
    asyncio.run(main())
