"""initial

Revision ID: 0a7e33b1ee32
Revises: 
Create Date: 2023-05-01 16:16:26.820868

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0a7e33b1ee32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('value', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    actions_table = sa.Table('actions', sa.MetaData(), autoload_with=op.get_bind())
    op.bulk_insert(actions_table, [
        {'id': 0, 'value': 'FP received'},
        {'id': 1, 'value': 'FP analyzed'},
        {'id': 2, 'value': 'Cookie sent'},
        {'id': 3, 'value': 'Cookie received'},
        {'id': 4, 'value': 'Cookie invalid'},
        {'id': 5, 'value': 'Bod detected'},
    ])

    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('uid', sa.UUID(), nullable=True),
                    sa.Column('ip', sa.String(), nullable=False),
                    sa.Column('fingerprint', sa.JSON(), nullable=True),
                    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
                    sa.Column('is_bot', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('uid')
                    )
    op.create_table('cookies',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('value', sa.UUID(), nullable=True),
                    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
                    sa.Column('expiration_time', sa.DateTime(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('value')
                    )
    op.create_table('logging',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('cookie_id', sa.Integer(), nullable=True),
                    sa.Column('action_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['action_id'], ['actions.id'], ),
                    sa.ForeignKeyConstraint(['cookie_id'], ['cookies.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logging')
    op.drop_table('cookies')
    op.drop_table('users')
    op.drop_table('actions')
    # ### end Alembic commands ###