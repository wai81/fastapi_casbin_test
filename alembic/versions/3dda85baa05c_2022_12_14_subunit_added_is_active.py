"""'2022_12_14_subunit_added_is_active'

Revision ID: 3dda85baa05c
Revises: cc8885643172
Create Date: 2022-12-14 21:52:26.385516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dda85baa05c'
down_revision = 'cc8885643172'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subunit', sa.Column('is_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subunit', 'is_active')
    # ### end Alembic commands ###
