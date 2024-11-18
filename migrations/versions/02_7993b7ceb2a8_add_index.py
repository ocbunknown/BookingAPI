"""add index

Revision ID: 02_7993b7ceb2a8
Revises: 01_3bfc9b76f933
Create Date: 2024-11-05 22:09:26.501194

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "02_7993b7ceb2a8"
down_revision: Union[str, None] = "01_3bfc9b76f933"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("user_email_key", "user", type_="unique")
    op.drop_constraint("user_phone_key", "user", type_="unique")
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_phone"), "user", ["phone"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_phone"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.create_unique_constraint("user_phone_key", "user", ["phone"])
    op.create_unique_constraint("user_email_key", "user", ["email"])
    # ### end Alembic commands ###