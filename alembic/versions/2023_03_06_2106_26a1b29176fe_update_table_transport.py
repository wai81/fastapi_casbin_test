"""update_table_Transport

Revision ID: 26a1b29176fe
Revises: 1233de0047c4
Create Date: 2023-03-06 21:06:14.513712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26a1b29176fe'
down_revision = '1233de0047c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transport', sa.Column('image_url', sa.String(), nullable=True))
    op.add_column('transport', sa.Column('image_url_type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transport', 'image_url_type')
    op.drop_column('transport', 'image_url')
    # ### end Alembic commands ###
