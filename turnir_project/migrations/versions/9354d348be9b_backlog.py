"""backlog

Revision ID: 9354d348be9b
Revises: 98590dab1623
Create Date: 2022-05-15 10:31:42.868242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9354d348be9b'
down_revision = '98590dab1623'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('backlogDB',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fighter_id', sa.Integer(), nullable=True),
    sa.Column('round_number', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fighter_id'], ['participantsDB.participant_id'], name=op.f('fk_backlogDB_fighter_id_participantsDB')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_backlogDB'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('backlogDB')
    # ### end Alembic commands ###
