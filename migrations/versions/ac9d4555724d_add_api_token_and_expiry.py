"""Add api token and expiry

Revision ID: ac9d4555724d
Revises: 
Create Date: 2024-11-01 10:56:05.827705

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ac9d4555724d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
       op.create_table(
              'users',
              sa.Column('id', sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
              sa.Column('username', sa.String(255), nullable=False, unique=True),
              sa.Column('email', sa.String(255), nullable=False, unique=True),
              sa.Column('password', sa.String(255), nullable=False),
              sa.Column('role_id', sa.SmallInteger(), nullable=False, server_default='1'), #Standard user permission level
              sa.Column('api_token', sa.String(255), nullable=True, unique=True),
              sa.Column('token_expiry', sa.DateTime(), nullable=True)
       )