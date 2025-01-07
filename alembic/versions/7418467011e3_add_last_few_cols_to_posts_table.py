"""add last few cols to posts table

Revision ID: 7418467011e3
Revises: 585d7a2da00a
Create Date: 2025-01-07 20:05:28.459159

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7418467011e3"
down_revision: Union[str, None] = "585d7a2da00a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="True"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_columns("posts", "published")
    op.drop_columns("posts", "created_at")
    pass
