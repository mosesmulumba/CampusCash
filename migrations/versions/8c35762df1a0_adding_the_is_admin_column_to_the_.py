"""adding the is_admin column to the students model

Revision ID: 8c35762df1a0
Revises: 5db200e79638
Create Date: 2025-04-01 23:35:26.734477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c35762df1a0'
down_revision = '5db200e79638'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###
