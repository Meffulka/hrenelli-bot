from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, BigInteger, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
import datetime
import json
from config import async_session
from datetime import datetime, timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    discord_id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    godname = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    level = Column(Integer, nullable=True)
    max_health = Column(Integer, nullable=True)
    inventory_max_num = Column(Integer, nullable=True)
    motto = Column(String, nullable=True)
    clan = Column(String, nullable=True)
    clan_position = Column(String, nullable=True)
    alignment = Column(String, nullable=True)
    bricks_cnt = Column(Integer, nullable=True)
    wood_cnt = Column(Integer, nullable=True)
    temple_completed_at = Column(DateTime, nullable=True)
    pet = Column(JSON, nullable=True)
    ark_completed_at = Column(DateTime, nullable=True)
    arena_won = Column(Integer, nullable=True)
    arena_lost = Column(Integer, nullable=True)
    savings = Column(String, nullable=True)
    health = Column(Integer, nullable=True)
    quest_progress = Column(Integer, nullable=True)
    exp_progress = Column(Integer, nullable=True)
    godpower = Column(Integer, nullable=True)
    gold_approx = Column(String, nullable=True)
    diary_last = Column(String, nullable=True)
    town_name = Column(String, nullable=True)
    distance = Column(Integer, nullable=True)
    arena_fight = Column(Boolean, nullable=True)
    inventory_num = Column(Integer, nullable=True)
    quest = Column(String, nullable=True)
    activatables = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    token = Column(String, nullable=True)


    def __init__(self, name, godname, discord_id, gender=None, level=None, max_health=None, inventory_max_num=None, motto=None, clan=None, clan_position=None, alignment=None, bricks_cnt=None, wood_cnt=None, temple_completed_at=None, pet=None, ark_completed_at=None, arena_won=None, arena_lost=None, savings=None, health=None, quest_progress=None, exp_progress=None, godpower=None, gold_approx=None, diary_last=None, town_name=None, distance=None, arena_fight=None, inventory_num=None, quest=None, activatables=None, token=None):
        self.discord_id = discord_id
        self.name = name
        self.godname = godname
        self.gender = gender
        self.level = level
        self.max_health = max_health
        self.inventory_max_num = inventory_max_num
        self.motto = motto
        self.clan = clan
        self.clan_position = clan_position
        self.alignment = alignment
        self.bricks_cnt = bricks_cnt
        self.wood_cnt = wood_cnt
        self.temple_completed_at = temple_completed_at
        self.pet = pet
        self.ark_completed_at = ark_completed_at
        self.arena_won = arena_won
        self.arena_lost = arena_lost
        self.savings = savings
        self.health = health
        self.quest_progress = quest_progress
        self.exp_progress = exp_progress
        self.godpower = godpower
        self.gold_approx = gold_approx
        self.diary_last = diary_last
        self.town_name = town_name
        self.distance = distance
        self.arena_fight = arena_fight
        self.inventory_num = inventory_num
        self.quest = quest
        self.activatables = activatables
        self.token = token


    @staticmethod
    def from_json(json_data, discord_id, token=None):
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        if json_data.get('temple_completed_at') is not None:
            json_data['temple_completed_at'] = datetime.fromisoformat(json_data['temple_completed_at']).replace(tzinfo=None)

        if json_data.get('ark_completed_at') is not None:
            json_data['ark_completed_at'] = datetime.fromisoformat(json_data['ark_completed_at']).replace(tzinfo=None)

        return User(**json_data, token=token, discord_id=discord_id)

    async def upsert_user(user_data, discord_id, token=None):
        try:
            user = User.from_json(user_data, discord_id=discord_id, token=token)
            async with async_session() as session:
                merged_user = await session.merge(user)
                await session.flush()
                await session.commit()
            return merged_user
        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении транзакции: {e}")
            await session.rollback()
            raise
        except Exception as e:
            print(f"{e}")

    async def get_first_user_not_updated_async():
        async with async_session() as session:
            now = datetime.utcnow()
            one_day_ago = now - timedelta(days=1)

            stmt = (
                select(User)
                .where(User.updated_at < one_day_ago)
                .order_by(User.updated_at)
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
        return user

    async def get_user_by_discord_id(discord_id):
        async with async_session() as session:
            stmt = select(User).where(User.discord_id == discord_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
        return user