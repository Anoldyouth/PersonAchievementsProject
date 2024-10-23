"""Create achievements table

Revision ID: 9d31ee4e294d
Revises: 9232559628c4
Create Date: 2024-10-24 01:13:31.755519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d31ee4e294d'
down_revision: Union[str, None] = '9232559628c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
table_name = "achievements"


def upgrade():
    op.create_table(
        table_name,
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('value', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
    )
    op.create_check_constraint(
        'non_negative_value',
        table_name,
        'value >= 0'
    )


def downgrade():
    op.drop_table(table_name)
