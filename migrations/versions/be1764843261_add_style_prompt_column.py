"""Add style_prompt column

Revision ID: be1764843261
Revises: 
Create Date: 2025-04-23 17:53:19.845864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be1764843261'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('style_image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('style_prompt', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('style_strength', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('style_image', schema=None) as batch_op:
        batch_op.drop_column('style_strength')
        batch_op.drop_column('style_prompt')

    # ### end Alembic commands ###
