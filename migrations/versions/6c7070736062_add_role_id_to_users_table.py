"""Add role_id to users table

Revision ID: 6c7070736062
Revises: ad8ca3c3dfaa
Create Date: 2025-01-06 20:16:19.191868

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6c7070736062'
down_revision = 'ad8ca3c3dfaa'
branch_labels = None
depends_on = None

def upgrade():
    # Add column role_id to users table
    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])

def downgrade():
    # Remove column role_id from users table
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
