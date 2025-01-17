"""Change depart_time and destination_time from DateTime to Time

Revision ID: ce28a5ddecee
Revises: 28932a02e785
Create Date: 2025-01-17 14:36:45.488306

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ce28a5ddecee'
down_revision = '28932a02e785'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('listing_images', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'listings', ['listing_id'], ['id'])

    with op.batch_alter_table('listings', schema=None) as batch_op:
        batch_op.alter_column('depart_time',
               existing_type=mysql.DATETIME(),
               type_=sa.Time(),
               existing_nullable=False)
        batch_op.alter_column('destination_time',
               existing_type=mysql.DATETIME(),
               type_=sa.Time(),
               existing_nullable=False)
