"""initial

Revision ID: 8f0941742b6c
Revises: 
Create Date: 2023-04-21 20:48:16.344964

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8f0941742b6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('codes',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.String(), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('code')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('uid', sa.UUID(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('code_id', sa.Integer(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['code_id'], ['codes.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('uid')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('codes')
    # ### end Alembic commands ###
