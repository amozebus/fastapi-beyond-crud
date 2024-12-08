"""create users table

Revision ID: 1f167c40b9a3
Revises: 
Create Date: 2024-12-09 00:07:12.393323

"""
import uuid

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f167c40b9a3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        sa.Column("uid", sa.UUID, nullable=False, unique=True, primary_key=True, default=uuid.uuid4),
        sa.Column("username", sa.VARCHAR, nullable=False, unique=True),
        sa.Column("password_hash", sa.VARCHAR, nullable=False)
    )


def downgrade() -> None:
    pass
