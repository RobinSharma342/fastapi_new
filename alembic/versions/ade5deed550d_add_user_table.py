"""add user table

Revision ID: ade5deed550d
Revises: 409e7a59253e
Create Date: 2022-08-16 21:49:14.104201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ade5deed550d'
down_revision = '409e7a59253e'
branch_labels = None
depends_on = None


def upgrade():
     op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True))
        
        

def downgrade() -> None:
    pass
