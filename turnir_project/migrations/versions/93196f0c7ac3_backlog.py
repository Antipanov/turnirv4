"""backlog

Revision ID: 93196f0c7ac3
Revises: 9354d348be9b
Create Date: 2022-05-15 11:02:02.249412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93196f0c7ac3'
down_revision = '9354d348be9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('backlogDB', schema=None) as batch_op:
        batch_op.add_column(sa.Column('competition_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_backlogDB_competition_id_competitionsDB'), 'competitionsDB', ['competition_id'], ['competition_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('backlogDB', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_backlogDB_competition_id_competitionsDB'), type_='foreignkey')
        batch_op.drop_column('competition_id')

    # ### end Alembic commands ###
