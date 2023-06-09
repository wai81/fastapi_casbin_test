"""update_bookingTransport_add_relathion_creator

Revision ID: eea2df1a76a1
Revises: de4e24a097ed
Create Date: 2023-04-06 21:26:59.455830

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eea2df1a76a1'
down_revision = 'de4e24a097ed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookingtransport', sa.Column('creator_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'bookingtransport', 'user', ['creator_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bookingtransport', type_='foreignkey')
    op.drop_column('bookingtransport', 'creator_id')
    # ### end Alembic commands ###
