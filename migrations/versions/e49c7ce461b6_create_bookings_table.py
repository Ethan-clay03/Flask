"""Create bookings table

Revision ID: e49c7ce461b6
Revises: 77815275598c
Create Date: 2025-01-08 17:08:51.080297

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'e49c7ce461b6'
down_revision = '77815275598c'
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    if 'bookings' not in inspector.get_table_names():
        op.create_table(
                'bookings',
                sa.Column('id', sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
                sa.Column('user_id', sa.Integer(), nullable=False),
                sa.Column('listing_id', sa.Integer(), nullable=False),
                sa.Column('amount_paid', sa.Integer(), nullable=False),
                sa.Column('cancelled', sa.Boolean(), nullable=False),
                sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ondelete='CASCADE'),
                sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
        )

        #Remove columns from listing as moved to new table
        op.drop_column('listings', 'economy_tickets') 
        op.drop_column('listings', 'business_tickets')

