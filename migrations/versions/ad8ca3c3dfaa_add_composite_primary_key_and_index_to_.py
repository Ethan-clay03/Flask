"""Add composite primary key and index to roles_users

Revision ID: ad8ca3c3dfaa
Revises: 22de5b143d05
Create Date: 2025-01-06 13:56:13.747100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad8ca3c3dfaa'
down_revision = '22de5b143d05'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('roles_users')
    
    op.create_table(
        'roles_users',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True, index=True),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id'), primary_key=True)
    )

def downgrade():
    op.drop_table('roles_users')
    
    op.create_table(
        'roles_users',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id'))
    )
