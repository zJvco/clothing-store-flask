"""empty message

Revision ID: 5cd6b0ed761d
Revises: eec64dc07612
Create Date: 2021-09-27 11:17:05.921537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cd6b0ed761d'
down_revision = 'eec64dc07612'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('adresses', 'complement',
               existing_type=sa.TEXT(length=500),
               type_=sa.String(length=140),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('adresses', 'complement',
               existing_type=sa.String(length=140),
               type_=sa.TEXT(length=500),
               existing_nullable=True)
    # ### end Alembic commands ###
