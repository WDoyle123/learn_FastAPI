"""add content column to posts table

Revision ID: 92b14c16e98e
Revises: 94306e4fb7c5
Create Date: 2025-01-07 19:41:44.342733

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "92b14c16e98e"
down_revision: Union[str, None] = "94306e4fb7c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
