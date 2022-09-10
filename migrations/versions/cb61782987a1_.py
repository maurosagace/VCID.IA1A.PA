"""empty message

Revision ID: cb61782987a1
Revises: d99379e8c882
Create Date: 2022-08-27 11:17:04.214087

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cb61782987a1'
down_revision = 'd99379e8c882'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('week',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('begin', sa.Date(), nullable=True),
    sa.Column('end', sa.Date(), nullable=True),
    sa.Column('reserved_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['reserved_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('period')
    op.drop_index('ix_user_address', table_name='user')
    op.drop_index('ix_user_phone', table_name='user')
    op.drop_column('user', 'phone')
    op.drop_column('user', 'address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('address', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('user', sa.Column('phone', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_index('ix_user_phone', 'user', ['phone'], unique=False)
    op.create_index('ix_user_address', 'user', ['address'], unique=False)
    op.create_table('period',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('begin', sa.DATE(), nullable=True),
    sa.Column('end', sa.DATE(), nullable=True),
    sa.Column('reserved_user', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['reserved_user'], ['user.id'], name='period_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('week')
    # ### end Alembic commands ###
