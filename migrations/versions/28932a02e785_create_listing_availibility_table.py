"""Create listing availibility table

Revision ID: 28932a02e785
Revises: e49c7ce461b6
Create Date: 2025-01-08 18:41:40.962877

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = '28932a02e785'
down_revision = 'e49c7ce461b6'
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    if 'listing_availability' not in inspector.get_table_names():
        op.create_table(
                'listing_availability',
                sa.Column('id', sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
                sa.Column('listing_id', sa.Integer(), nullable=False),
                sa.Column('business_tickets', sa.Integer(), nullable=False),
                sa.Column('economy_tickets', sa.Integer(), nullable=False),
                sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ondelete='CASCADE')
        )
