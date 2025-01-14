"""Add listing images table

Revision ID: 489bab9aaf4f
Revises: 6791cbf31235
Create Date: 2024-11-05 11:13:50.215159

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '489bab9aaf4f'
down_revision = '6791cbf31235'
branch_labels = None
depends_on = None


def upgrade():
       bind = op.get_bind()
       inspector = Inspector.from_engine(bind)

       # Check if the 'users' table exists
       if 'listing_images' not in inspector.get_table_names():
              op.create_table(
                     'listing_images',
                     sa.Column('id', sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
                     sa.Column('listing_id', sa.Integer(), nullable=False),
                     sa.Column('image_location', sa.String(255), nullable=False),
                     sa.Column('image_description', sa.String(255), nullable=True)
              )
