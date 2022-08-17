"""create post table

Revision ID: 173db440ab9f
Revises: 
Create Date: 2022-08-16 20:04:04.843612

"""
from datetime import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '173db440ab9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():



    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False))
        

def downgrade():
    op.drop_table('posts')
