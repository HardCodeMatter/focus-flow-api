"""Add due_date column for Task model

Revision ID: 278cf056672a
Revises: 674d2b9f7aae
Create Date: 2025-02-03 21:15:47.559603

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "278cf056672a"
down_revision: Union[str, None] = "674d2b9f7aae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("tasks", sa.Column("due_date", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("tasks", "due_date")
    # ### end Alembic commands ###
