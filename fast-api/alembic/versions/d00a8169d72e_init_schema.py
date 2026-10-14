"""init_schema

Revision ID: d00a8169d72e
Revises: 
Create Date: 2026-10-14 09:22:25.532086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd00a8169d72e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE title_basics
        (
            tconst          text PRIMARY KEY,
            title_type      text,
            primary_title   text,
            original_title  text,
            is_adult        boolean,
            start_year      integer null,
            end_year        integer null,
            runtime_minutes integer null,
            genres          text
        );

        CREATE TABLE title_ratings
        (
            tconst         text PRIMARY KEY,
            average_rating numeric(3, 1),
            num_votes      integer
        );

        """)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DROP TABLE title_basics;
        DROP TABLE title_ratings;
        """)
    pass
