"""add_pgvector

Revision ID: d979f9b1c1b7
Revises: 001
Create Date: 2026-06-28 15:42:18.671642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = 'd979f9b1c1b7'
down_revision: Union[str, Sequence[str], None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    op.add_column('jobs', sa.Column('embedding', Vector(384), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('jobs', 'embedding')
    op.execute('DROP EXTENSION IF EXISTS vector')
