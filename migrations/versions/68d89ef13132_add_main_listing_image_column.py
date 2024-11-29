"""Add main Listing Image Column

Revision ID: 68d89ef13132
Revises: 489bab9aaf4f
Create Date: 2024-11-29 10:29:38.126811

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '68d89ef13132'
down_revision = '489bab9aaf4f'
branch_labels = None
depends_on = None


def upgrade():
        op.add_column(
        'listing_images',
        sa.Column('main_image', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false())
    )