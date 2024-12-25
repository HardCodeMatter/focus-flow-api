"""Created Priority field for Task

Revision ID: f06b26ad9546
Revises: 00a84d4140e8
Create Date: 2024-12-25 23:41:21.514993

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f06b26ad9546"
down_revision: Union[str, None] = "00a84d4140e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tasks",
        sa.Column(
            "priority",
            sa.Enum("low", "medium", "high", name="priority"),
            server_default="low",
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("tasks", "priority")
    # ### end Alembic commands ###