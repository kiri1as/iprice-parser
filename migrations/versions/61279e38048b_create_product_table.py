"""create product table

Revision ID: 61279e38048b
Revises: 
Create Date: 2024-12-28 13:06:42.220608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '61279e38048b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with open('migrations/sql/init_product_table.sql', 'r') as script:
        init_script = script.read()
    op.execute(init_script)


def downgrade() -> None:
    with open('migrations/sql/drop_prouct_table.sql', 'r') as script:
        downgrade_script = script.read()
    op.execute(downgrade_script)
