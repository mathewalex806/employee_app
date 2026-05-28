"""init

Revision ID: 947401459a5a
Revises: ec6c794ecf84
Create Date: 2026-05-28 17:14:39.547980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '947401459a5a'
down_revision: Union[str, Sequence[str], None] = 'ec6c794ecf84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
