"""Create users table

Revision ID: 9232559628c4
Revises: 
Create Date: 2024-10-24 01:04:59.915393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.models.user import LanguageEnum

# revision identifiers, used by Alembic.
revision: str = '9232559628c4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
table_name = "users"


def upgrade():
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('lang', sa.Enum(LanguageEnum), nullable=False)
    )


def downgrade():
    op.drop_table(table_name)
