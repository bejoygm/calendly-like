"""event id for booking

Revision ID: 7a34d44ec206
Revises: 71313c4fcb2f
Create Date: 2024-06-26 12:56:45.357671

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7a34d44ec206"
down_revision = "71313c4fcb2f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("booking", sa.Column("event_id", sa.String(), nullable=False))
    op.create_foreign_key(
        op.f("booking_event_id_fkey"), "booking", "event", ["event_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("booking_event_id_fkey"), "booking", type_="foreignkey")
    op.drop_column("booking", "event_id")
    # ### end Alembic commands ###
