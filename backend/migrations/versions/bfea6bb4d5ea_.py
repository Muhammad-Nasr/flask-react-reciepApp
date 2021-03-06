"""empty message

Revision ID: bfea6bb4d5ea
Revises: 6c854fc9917d
Create Date: 2022-07-04 22:20:21.540303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfea6bb4d5ea'
down_revision = '6c854fc9917d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'recipe', 'user', ['user_id'], ['id'])
    op.create_unique_constraint(None, 'user', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'recipe', type_='foreignkey')
    # ### end Alembic commands ###
