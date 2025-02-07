"""create users table

Revision ID: 1f167c40b9a3
Revises: 
Create Date: 2024-12-09 00:07:12.393323

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1f167c40b9a3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer,
            nullable=False,
            unique=True,
            primary_key=True,
        ),
        sa.Column("username", sa.VARCHAR, nullable=False, unique=True),
        sa.Column("password_hash", sa.VARCHAR, nullable=False),
        if_not_exists=True,
    )


def downgrade() -> None:
    op.drop_table("users", if_exists=True)
