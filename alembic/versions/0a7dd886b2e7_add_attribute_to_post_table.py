"""add attribute to post table

Revision ID: 0a7dd886b2e7
Revises: 7500f3a81f81
Create Date: 2022-08-16 22:08:53.311158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a7dd886b2e7'
down_revision = '7500f3a81f81'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    
    op.add_column('posts', sa.Column(
    'user_id', sa.Integer(), nullable=False))

    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    
        


def downgrade():
    op.drop_constraint('post_user_fk', 'posts')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'user_id')
    
