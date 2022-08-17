"""add user table

Revision ID: 7500f3a81f81
Revises: ade5deed550d
Create Date: 2022-08-16 21:55:56.698053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7500f3a81f81'
down_revision = 'ade5deed550d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP
        (timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        
        
        
        )


def downgrade():
    op.drop_table('users')
    pass
