"""Create phone number on users table

Revision ID: 224b70c078c8
Revises: 
Create Date: 2024-08-23 22:13:33.996931

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "224b70c078c8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
