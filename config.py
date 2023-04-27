from dotenv import load_dotenv
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

load_dotenv()

LOG_CHANNEL = os.getenv("LOG_CHANNEL")
CROSS_CHANNEL = os.getenv("CROSS_CHANNEL")
WELCOM_CHANNEL = os.getenv("WELCOM_CHANNEL")
SERVER_ID = os.getenv("SERVER_ID")

GOD_ALIGNMENTS_GOOD_LIST = ["беззлобный", "добродушный", "миролюбивый", "добродетельный", "абсолютное добро", "абсолютное добро!"]
CLAN_POSITIONS_LIST = ["фанат", "рекрут", "стажер", "адепт", "мастер", "магистр", "советник", "грандмастер", "кардинал", "иерарх", "патриарх", "регент", "пророк", "капореджиме"]

DC_TOKEN = os.getenv("DC_TOKEN")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL,echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)