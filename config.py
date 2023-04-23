from dotenv import load_dotenv
import os

load_dotenv()

LOG_CHANNEL = os.getenv("LOG_CHANNEL")
WELCOM_CHANNEL = os.getenv("WELCOM_CHANNEL")
SERVER_ID = os.getenv("SERVER_ID")

GOD_ALIGNMENTS_GOOD_LIST = ["беззлобный", "добродушный", "миролюбивый", "добродетельный", "абсолютное добро", "абсолютное добро!"]
CLAN_POSITIONS_LIST = ["фанат", "рекрут", "стажер", "адепт", "мастер", "магистр", "советник", "грандмастер", "кардинал", "иерарх", "патриарх", "регент", "пророк", "капореджиме"]

DC_TOKEN = os.getenv("DC_TOKEN")