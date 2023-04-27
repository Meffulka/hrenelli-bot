"""create initial user table

Revision ID: 61842257bc72
Revises:
Create Date: 2023-04-26 12:17:07.154993

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = '61842257bc72'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('discord_id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('godname', sa.String, nullable=False),
        sa.Column('gender', sa.String, nullable=True),
        sa.Column('level', sa.Integer, nullable=True),
        sa.Column('max_health', sa.Integer, nullable=True),
        sa.Column('inventory_max_num', sa.Integer, nullable=True),
        sa.Column('motto', sa.String, nullable=True),
        sa.Column('clan', sa.String, nullable=True),
        sa.Column('clan_position', sa.String, nullable=True),
        sa.Column('alignment', sa.String, nullable=True),
        sa.Column('bricks_cnt', sa.Integer, nullable=True),
        sa.Column('wood_cnt', sa.Integer, nullable=True),
        sa.Column('temple_completed_at', sa.DateTime, nullable=True),
        sa.Column('pet', sa.JSON, nullable=True),
        sa.Column('ark_completed_at', sa.DateTime, nullable=True),
        sa.Column('arena_won', sa.Integer, nullable=True),
        sa.Column('arena_lost', sa.Integer, nullable=True),
        sa.Column('savings', sa.String, nullable=True),
        sa.Column('health', sa.Integer, nullable=True),
        sa.Column('quest_progress', sa.Integer, nullable=True),
        sa.Column('exp_progress', sa.Integer, nullable=True),
        sa.Column('godpower', sa.Integer, nullable=True),
        sa.Column('gold_approx', sa.String, nullable=True),
        sa.Column('diary_last', sa.String, nullable=True),
        sa.Column('town_name', sa.String, nullable=True),
        sa.Column('distance', sa.Integer, nullable=True),
        sa.Column('arena_fight', sa.Boolean, nullable=True),
        sa.Column('inventory_num', sa.Integer, nullable=True),
        sa.Column('quest', sa.String, nullable=True),
        sa.Column('activatables', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow),
        sa.Column('token', sa.String, nullable=True),
    )



def downgrade() -> None:
    op.drop_table('users')
