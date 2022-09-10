"""Tabelle weeks

Revision ID: 2c88e43a9cdd
Revises: cb61782987a1
Create Date: 2022-08-27 12:53:58.870586

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2c88e43a9cdd'
down_revision = 'cb61782987a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weeks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_begin', sa.Date(), nullable=True),
    sa.Column('date_end', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('week')
    op.add_column('user', sa.Column('familyname', sa.String(length=64), nullable=True))
    op.drop_index('ix_user_lastname', table_name='user')
    op.create_index(op.f('ix_user_familyname'), 'user', ['familyname'], unique=False)
    op.drop_column('user', 'lastname')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('lastname', mysql.VARCHAR(length=64), nullable=True))
    op.drop_index(op.f('ix_user_familyname'), table_name='user')
    op.create_index('ix_user_lastname', 'user', ['lastname'], unique=False)
    op.drop_column('user', 'familyname')
    op.create_table('week',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('begin', sa.DATE(), nullable=True),
    sa.Column('end', sa.DATE(), nullable=True),
    sa.Column('reserved_user', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['reserved_user'], ['user.id'], name='week_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('weeks')
    # ### end Alembic commands ###