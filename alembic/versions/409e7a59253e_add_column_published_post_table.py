"""add column published post table

Revision ID: 409e7a59253e
Revises: 173db440ab9f
Create Date: 2022-08-16 21:25:24.866372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '409e7a59253e'
down_revision = '173db440ab9f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), nullable = False, server_default= 'True')
    )


def downgrade():
    op.drop_column('posts',
                'published'
    )
    
