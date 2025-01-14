"""Add api token and expiry

Revision ID: ac9d4555724d
Revises: 
Create Date: 2024-11-01 10:56:05.827705

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'ac9d4555724d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    # Check if the 'users' table exists
    if 'users' not in inspector.get_table_names():
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
            sa.Column('username', sa.String(255), nullable=False, unique=True),
            sa.Column('email', sa.String(255), nullable=False, unique=True),
            sa.Column('password', sa.String(255), nullable=False),
            sa.Column('role_id', sa.SmallInteger(), nullable=False, server_default='3')
        )

def downgrade():
    op.drop_table('users')
