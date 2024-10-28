"""Create users_achievements table

Revision ID: f19d31bcef62
Revises: 9d31ee4e294d
Create Date: 2024-10-24 01:20:44.122070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f19d31bcef62'
down_revision: Union[str, None] = '9d31ee4e294d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
table_name = 'users_achievements'


def upgrade() -> None:
    op.create_table(
        table_name,
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('achievement_id', sa.Integer, sa.ForeignKey('achievements.id'), primary_key=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table(table_name)
